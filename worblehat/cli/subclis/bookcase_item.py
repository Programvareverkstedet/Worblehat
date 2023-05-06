from textwrap import dedent
from sqlalchemy import select

from sqlalchemy.orm import Session

from worblehat.cli.prompt_utils import (
    InteractiveItemSelector,
    NumberedCmd,
    prompt_yes_no,
)
from worblehat.models import (
    Bookcase,
    BookcaseItem,
    Language,
    MediaType,
)
from worblehat.services.bookcase_item import (
    create_bookcase_item_from_isbn,
    is_valid_isbn,
)

from .bookcase_shelf_selector import select_bookcase_shelf

def _selected_bookcase_item_prompt(bookcase_item: BookcaseItem) -> str:
    return dedent(f'''
      Item: {bookcase_item.name}
        ISBN: {bookcase_item.isbn}
        Amount: {bookcase_item.amount}
        Authors: {', '.join(a.name for a in bookcase_item.authors)}
        Bookcase: {bookcase_item.shelf.bookcase.short_str()}
        Shelf: {bookcase_item.shelf.short_str()}
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


    def do_loan(self, arg: str):
        print('TODO: implement loan')


    def do_done(self, _: str):
        return True


    funcs = {
        1: {
            'f': do_loan,
            'doc': 'Loan',
        },
        2: {
            'f': do_edit,
            'doc': 'Edit',
        },
        3: {
            'f': do_update_data,
            'doc': 'Pull updated data from online databases',
        },
        4: {
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
        7: {
            'f': do_done,
            'doc': 'Done',
        },
    }

