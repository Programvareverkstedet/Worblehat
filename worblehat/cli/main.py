from textwrap import dedent

from sqlalchemy import (
   create_engine,
   event,
   select,
)
from sqlalchemy.orm import (
   Session,
)

from worblehat.services.bookcase_item import (
    create_bookcase_item_from_isbn,
    is_valid_isbn,
)

from .prompt_utils import *

from worblehat.config import Config
from worblehat.models import *

from .subclis.bookcase_item import BookcaseItemCli
from .subclis.bookcase_shelf_selector import select_bookcase_shelf

# TODO: Category seems to have been forgotten. Maybe relevant interactivity should be added?
#       However, is there anyone who are going to search by category rather than just look in
#       the shelves?

class WorblehatCli(NumberedCmd):
    sql_session: Session
    sql_session_dirty: bool = False

    def __init__(self):
        super().__init__()

        try:
            engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
            self.sql_session = Session(engine)
        except Exception:
            print('Error: could not connect to database.')
            exit(1)

        @event.listens_for(self.sql_session, 'after_flush')
        def mark_session_as_dirty(*_):
            self.sql_session_dirty = True
            self.prompt_header = f'(unsaved changes)'

        @event.listens_for(self.sql_session, 'after_commit')
        @event.listens_for(self.sql_session, 'after_rollback')
        def mark_session_as_clean(*_):
            self.sql_session_dirty = False
            self.prompt_header = None

        print(f"Debug: Connected to database at '{Config.SQLALCHEMY_DATABASE_URI}'")


    def do_list_bookcases(self, _: str):
        bookcase_shelfs = self.sql_session.scalars(
            select(BookcaseShelf)
            .join(Bookcase)
            .order_by(
              Bookcase.name,
              BookcaseShelf.column,
              BookcaseShelf.row,
            )
        ).all()

        bookcase_uid = None
        for shelf in bookcase_shelfs:
            if shelf.bookcase.uid != bookcase_uid:
                print(shelf.bookcase.short_str())
                bookcase_uid = shelf.bookcase.uid

            print(f'  {shelf.short_str()} - {sum(i.amount for i in shelf.items)} items')


    def do_show_bookcase(self, arg: str):
        bookcase_selector = InteractiveItemSelector(
            cls = Bookcase,
            sql_session = self.sql_session,
        )
        bookcase_selector.cmdloop()
        bookcase = bookcase_selector.result

        for shelf in bookcase.shelfs:
            print(shelf.short_str())
            for item in shelf.items:
                print(f'  {item.name} - {item.amount} copies')


    def do_add_bookcase(self, _: str):
        while True:
            name = input('Name of bookcase> ')
            if name == '':
                print('Error: name cannot be empty')
                continue

            if self.sql_session.scalars(
                select(Bookcase)
                .where(Bookcase.name == name)
            ).one_or_none() is not None:
                print(f'Error: a bookcase with name {name} already exists')
                continue

            break

        description = input('Description of bookcase> ')
        if description == '':
            description = None

        bookcase = Bookcase(name, description)
        self.sql_session.add(bookcase)
        self.sql_session.flush()


    def do_add_bookcase_shelf(self, arg: str):
        bookcase_selector = InteractiveItemSelector(
            cls = Bookcase,
            sql_session = self.sql_session,
        )
        bookcase_selector.cmdloop()
        bookcase = bookcase_selector.result

        while True:
            column = input('Column> ')
            try:
                column = int(column)
            except ValueError:
                print('Error: column must be a number')
                continue
            break

        while True:
            row = input('Row> ')
            try:
                row = int(row)
            except ValueError:
                print('Error: row must be a number')
                continue
            break

        if self.sql_session.scalars(
            select(BookcaseShelf)
            .where(
              BookcaseShelf.bookcase == bookcase,
              BookcaseShelf.column == column,
              BookcaseShelf.row == row,
            )
        ).one_or_none() is not None:
            print(f'Error: a bookshelf in bookcase {bookcase.name} with position c{column}-r{row} already exists')
            return

        description = input('Description> ')
        if description == '':
            description = None

        shelf = BookcaseShelf(
            row,
            column,
            bookcase,
            description,
        )
        self.sql_session.add(shelf)
        self.sql_session.flush()


    def _create_bookcase_item(self, isbn: str):
        bookcase_item = create_bookcase_item_from_isbn(isbn, self.sql_session)
        if bookcase_item is None:
            print(f'Could not find data about item with ISBN {isbn} online.')
            print(f'If you think this is not due to a bug, please add the book to openlibrary.org before continuing.')
            return
        else:
            print(dedent(f"""
            Found item:
              title: {bookcase_item.name}
              authors: {', '.join(a.name for a in bookcase_item.authors)}
              language: {bookcase_item.language}
            """))

        print('Please select the bookcase where the item is placed:')
        bookcase_selector = InteractiveItemSelector(
            cls = Bookcase,
            sql_session = self.sql_session,
        )
        bookcase_selector.cmdloop()
        bookcase = bookcase_selector.result

        bookcase_item.shelf = select_bookcase_shelf(bookcase, self.sql_session)

        print('Please select the items media type:')
        media_type_selector = InteractiveItemSelector(
            cls = MediaType,
            sql_session = self.sql_session,
            default = self.sql_session.scalars(
              select(MediaType)
              .where(MediaType.name.ilike("book")),
            ).one(),
        )

        media_type_selector.cmdloop()
        bookcase_item.media_type = media_type_selector.result

        username = input('Who owns this book? [PVV]> ')
        if username != '':
            bookcase_item.owner = username

        self.sql_session.add(bookcase_item)
        self.sql_session.flush()


    def default(self, isbn: str):
        isbn = isbn.strip()
        if not is_valid_isbn(isbn):
            super()._default(isbn)
            return

        if (existing_item := self.sql_session.scalars(
            select(BookcaseItem)
            .where(BookcaseItem.isbn == isbn)
        ).one_or_none()) is not None:
            print(f'\nFound existing item for isbn "{isbn}"')
            BookcaseItemCli(
                sql_session = self.sql_session,
                bookcase_item = existing_item,
            ).cmdloop()
            return

        if prompt_yes_no(f"Could not find item with ISBN '{isbn}'.\nWould you like to create it?", default=True):
            self._create_bookcase_item(isbn)


    def do_search(self, _: str):
        print('TODO: implement search')

    def do_save(self, _:str):
        if not self.sql_session_dirty:
            print('No changes to save.')
            return
        self.sql_session.commit()


    def do_abort(self, _:str):
        if not self.sql_session_dirty:
            print('No changes to abort.')
            return
        self.sql_session.rollback()


    def do_exit(self, _: str):
        if self.sql_session_dirty:
           if prompt_yes_no('Would you like to save your changes?'):
               self.sql_session.commit()
           else:
               self.sql_session.rollback()
        exit(0)


    funcs = {
        0: {
            'f': default,
            'doc': 'Choose / Add item with its ISBN',
        },
        1: {
            'f': do_list_bookcases,
            'doc': 'List all bookcases',
        },
        2: {
            'f': do_search,
            'doc': 'Search',
        },
        3: {
            'f': do_show_bookcase,
            'doc': 'Show a bookcase, and its items',
        },
        4: {
            'f': do_add_bookcase,
            'doc': 'Add a new bookcase',
        },
        5: {
            'f': do_add_bookcase_shelf,
            'doc': 'Add a new bookshelf',
        },
        6: {
            'f': do_save,
            'doc': 'Save changes',
        },
        7: {
            'f': do_abort,
            'doc': 'Abort changes',
        },
        8: {
            'f': do_exit,
            'doc': 'Exit',
        },
    }


def main():
    tool = WorblehatCli()
    while True:
        try:
            tool.cmdloop()
        except KeyboardInterrupt:
            if not tool.sql_session_dirty:
                exit(0)
            try:
              print()
              if prompt_yes_no('Are you sure you want to exit without saving?', default=False):
                  raise KeyboardInterrupt
            except KeyboardInterrupt:
                if tool.sql_session is not None:
                    tool.sql_session.rollback()
                exit(0)

if __name__ == '__main__':
    main()