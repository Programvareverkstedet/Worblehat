from textwrap import dedent
from sqlalchemy import select

from sqlalchemy.orm import Session

from worblehat.cli.prompt_utils import (
    InteractiveItemSelector,
    NumberedCmd,
    format_date,
    prompt_yes_no,
)
from worblehat.models import (
    Bookcase,
    BookcaseItem,
    BookcaseItemBorrowing,
    BookcaseItemBorrowingQueue,
    Language,
    MediaType,
)
from worblehat.services.bookcase_item import (
    create_bookcase_item_from_isbn,
    is_valid_isbn,
)

from .bookcase_shelf_selector import select_bookcase_shelf

def _selected_bookcase_item_prompt(bookcase_item: BookcaseItem) -> str:
    amount_borrowed = len(bookcase_item.borrowings)
    return dedent(f'''
      Item: {bookcase_item.name}
        ISBN: {bookcase_item.isbn}
        Authors: {', '.join(a.name for a in bookcase_item.authors)}
        Bookcase: {bookcase_item.shelf.bookcase.short_str()}
        Shelf: {bookcase_item.shelf.short_str()}
        Amount: {bookcase_item.amount - amount_borrowed}/{bookcase_item.amount}
    ''')

class BookcaseItemCli(NumberedCmd):
    def __init__(self, sql_session: Session, bookcase_item: BookcaseItem):
        super().__init__()
        self.sql_session = sql_session
        self.bookcase_item = bookcase_item


    @property
    def prompt_header(self) -> str:
        return _selected_bookcase_item_prompt(self.bookcase_item)


    def do_update_data(self, _: str):
        item = create_bookcase_item_from_isbn(self.sql_session, self.bookcase_item.isbn)
        self.bookcase_item.name = item.name
        # TODO: Remove any old authors
        self.bookcase_item.authors = item.authors
        self.bookcase_item.language = item.language


    def do_edit(self, arg: str):
        EditBookcaseCli(self.sql_session, self.bookcase_item, self).cmdloop()


    @staticmethod
    def _prompt_username() -> str:
        while True:
            username = input('Username: ')
            if prompt_yes_no(f'Is {username} correct?', default = True):
                return username


    def _has_active_borrowing(self, username: str) -> bool:
        return self.sql_session.scalars(
            select(BookcaseItemBorrowing)
            .where(
                BookcaseItemBorrowing.username == username,
                BookcaseItemBorrowing.item == self.bookcase_item,
                BookcaseItemBorrowing.delivered != True,
            )
        ).one_or_none() is not None


    def _has_borrowing_queue_item(self, username: str) -> bool:
        return self.sql_session.scalars(
            select(BookcaseItemBorrowingQueue)
            .where(
                BookcaseItemBorrowingQueue.username == username,
                BookcaseItemBorrowingQueue.item == self.bookcase_item,
            )
        ).one_or_none() is not None


    def do_borrow(self, _: str):
        active_borrowings = self.sql_session.scalars(
            select(BookcaseItemBorrowing)
            .where(
              BookcaseItemBorrowing.item == self.bookcase_item,
              BookcaseItemBorrowing.delivered != True,
            )
            .order_by(BookcaseItemBorrowing.end_time)
        ).all()

        if len(active_borrowings) >= self.bookcase_item.amount:
            print('This item is currently not available')
            print()
            print('Active borrowings:')

            for b in active_borrowings:
                print(f'  {b.username} - Until {format_date(b.end_time)}')

            if len(self.bookcase_item.borrowing_queue) > 0:
                print('Borrowing queue:')
                for i, b in enumerate(self.bookcase_item.borrowing_queue):
                    print(f'  {i + 1} - {b.username}')

            print()

            if not prompt_yes_no('Would you like to enter the borrowing queue?', default = True):
                return
            username = self._prompt_username()

            if self._has_active_borrowing(username):
                print('You already have an active borrowing')
                return

            if self._has_borrowing_queue_item(username):
                print('You are already in the borrowing queue')
                return

            borrowing_queue_item = BookcaseItemBorrowingQueue(username, self.bookcase_item)
            self.sql_session.add(borrowing_queue_item)
            print(f'{username} entered the queue!')
            return

        username = self._prompt_username()

        borrowing_item = BookcaseItemBorrowing(username, self.bookcase_item)
        self.sql_session.add(borrowing_item)
        print(f'Successfully delivered the item. Please deliver it back by {format_date(borrowing_item.end_time)}')

    def do_deliver(self, _: str):
        borrowings = self.sql_session.scalars(
            select(BookcaseItemBorrowing)
            .join(BookcaseItem, BookcaseItem.uid == BookcaseItemBorrowing.fk_bookcase_item_uid)
            .where(BookcaseItem.isbn == self.bookcase_item.isbn)
            .order_by(BookcaseItemBorrowing.username)
        ).all()

        if len(borrowings) == 0:
            print('No one seems to have borrowed this item')
            return

        print('Borrowers:')
        for i, b in enumerate(borrowings):
            print(f'  {i + 1}) {b.username}')

        while True:
            try:
                selection = int(input('> '))
            except ValueError:
                print('Error: selection must be an integer')
                continue

            if selection < 1 or selection > len(borrowings):
                print('Error: selection out of range')
                continue

            break

        borrowing = borrowings[selection - 1]
        borrowing.delivered = True
        print(f'Successfully delivered the item for {borrowing.username}')


    def do_done(self, _: str):
        return True


    funcs = {
        1: {
            'f': do_borrow,
            'doc': 'Borrow',
        },
        2: {
            'f': do_deliver,
            'doc': 'Deliver',
        },
        3: {
            'f': do_edit,
            'doc': 'Edit',
        },
        4: {
            'f': do_update_data,
            'doc': 'Pull updated data from online databases',
        },
        9: {
            'f': do_done,
            'doc': 'Done',
        },
    }

class EditBookcaseCli(NumberedCmd):
    def __init__(self, sql_session: Session, bookcase_item: BookcaseItem, parent: BookcaseItemCli):
        super().__init__()
        self.sql_session = sql_session
        self.bookcase_item = bookcase_item
        self.parent = parent

    @property
    def prompt_header(self) -> str:
      return _selected_bookcase_item_prompt(self.bookcase_item)

    def do_name(self, _: str):
        while True:
            name = input('New name> ')
            if name == '':
                print('Error: name cannot be empty')
                continue

            if self.sql_session.scalars(
                select(BookcaseItem)
                .where(BookcaseItem.name == name)
            ).one_or_none() is not None:
                print(f'Error: an item with name {name} already exists')
                continue

            break
        self.bookcase_item.name = name


    def do_isbn(self, _: str):
        while True:
            isbn = input('New ISBN> ')
            if isbn == '':
                print('Error: ISBN cannot be empty')
                continue

            if not is_valid_isbn(isbn):
                print('Error: ISBN is not valid')
                continue

            if self.sql_session.scalars(
                select(BookcaseItem)
                .where(BookcaseItem.isbn == isbn)
            ).one_or_none() is not None:
                print(f'Error: an item with ISBN {isbn} already exists')
                continue

            break

        self.bookcase_item.isbn = isbn

        if prompt_yes_no('Update data from online databases?'):
            self.parent.do_update_data('')


    def do_language(self, _: str):
        language_selector = InteractiveItemSelector(
            Language,
            self.sql_session,
        )

        self.bookcase_item.language = language_selector.result


    def do_media_type(self, _: str):
        media_type_selector = InteractiveItemSelector(
            MediaType,
            self.sql_session,
        )

        self.bookcase_item.media_type = media_type_selector.result


    def do_amount(self, _: str):
        while (new_amount := input(f'New amount [{self.bookcase_item.amount}]> ')) != '':
            try:
                new_amount = int(new_amount)
            except ValueError:
                print('Error: amount must be an integer')
                continue

            if new_amount < 1:
                print('Error: amount must be greater than 0')
                continue

            break
        self.bookcase_item.amount = new_amount


    def do_shelf(self, _: str):
        bookcase_selector = InteractiveItemSelector(
            Bookcase,
            self.sql_session,
        )
        bookcase_selector.cmdloop()
        bookcase = bookcase_selector.result

        shelf = select_bookcase_shelf(bookcase, self.sql_session)

        self.bookcase_item.shelf = shelf


    def do_done(self, _: str):
        return True


    funcs = {
        1: {
            'f': do_name,
            'doc': 'Change name',
        },
        2: {
            'f': do_isbn,
            'doc': 'Change ISBN',
        },
        3: {
            'f': do_language,
            'doc': 'Change language',
        },
        4: {
            'f': do_media_type,
            'doc': 'Change media type',
        },
        5: {
            'f': do_amount,
            'doc': 'Change amount',
        },
        6: {
            'f': do_shelf,
            'doc': 'Change shelf',
        },
        9: {
            'f': do_done,
            'doc': 'Done',
        },
    }

