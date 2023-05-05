from cmd import Cmd
from typing import Any
from textwrap import dedent

from sqlalchemy import (
   create_engine,
   select,
)
from sqlalchemy.orm import (
   Session,
)

from worblehat.services.bookcase_item import (
    create_bookcase_item_from_isbn,
    is_valid_isbn,
)

from ..config import Config
from ..models import *


def _prompt_yes_no(question: str, default: bool | None = None) -> bool:
    prompt = {
        None: '[y/n]',
        True: '[Y/n]',
        False: '[y/N]',
    }[default]

    while not any([
        (answer := input(f'{question} {prompt} ').lower()) in ('y','n'),
        (default != None and answer.strip() == '')
    ]):
        pass

    return {
        'y': True,
        'n': False,
        '': default,
    }[answer]


class _InteractiveItemSelector(Cmd):
    def __init__(
        self,
        cls: type,
        sql_session: Session,
        default: Any | None = None,
    ):
        super().__init__()
        self.cls = cls
        self.sql_session = sql_session
        self.default_item = default
        if default is not None:
          self.prompt = f'Select {cls.__name__} [{default.name}]> '
        else:
          self.prompt = f'Select {cls.__name__}> '

    def default(self, arg: str):
        if arg == '' and self.default_item is not None:
            self.result = self.default_item
            return True

        result = self.sql_session.scalars(
            select(self.cls)
            .where(self.cls.name == arg),
        ).all()

        if len(result) != 1:
            print(f'No such {self.cls.__name__} found: {arg}')
            return

        self.result = result[0]
        return True

    def completenames(self, text: str, *_) -> list[str]:
        return self.sql_session.scalars(
            select(self.cls.name)
            .where(self.cls.name.like(f'{text}%')),
        ).all()


class BookScanTool(Cmd):
    prompt = '> '
    intro = """
Welcome to the worblehat scanner tool.
Start by entering a command, or entering an ISBN of a new item.
Type "help" to see list of commands
    """

    def __init__(self):
        super().__init__()

        try:
            engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
            self.sql_session = Session(engine)
        except Exception:
            print('Error: could not connect to database.')
            exit(1)

        print(f"Connected to database at '{Config.SQLALCHEMY_DATABASE_URI}'")


    def do_list_bookcases(self, _: str):
        """Usage: list_bookcases"""
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
                print(shelf.bookcase.name)
                bookcase_uid = shelf.bookcase.uid

            name = f"r{shelf.row}-c{shelf.column}"
            if shelf.description is not None:
                 name += f" [{shelf.description}]"

            print(f'  {name} - {sum(i.amount for i in shelf.items)} items')


    def do_add_bookcase(self, arg: str):
        """Usage: add_bookcase <name> [description]"""
        arg = arg.split(' ')
        if len(arg) < 1:
            print('Usage: add_bookcase <name> [description]')
            return

        name = arg[0]
        description = ' '.join(arg[1:])

        if self.sql_session.scalars(
            select(Bookcase)
            .where(Bookcase.name == name)
        ).one_or_none() is not None:
            print(f'Error: a bookcase with name {name} already exists')
            return

        bookcase = Bookcase(name, description)
        self.sql_session.add(bookcase)

    def do_add_bookcase_shelf(self, arg: str):
        """Usage: add_bookcase_shelf <bookcase_name> <row>-<column> [description]"""
        arg = arg.split(' ')
        if len(arg) < 2:
            print('Usage: add_bookcase_shelf <bookcase_name> <row>-<column> [description]')
            return

        bookcase_name = arg[0]
        row, column = [int(x) for x in arg[1].split('-')]
        description = ' '.join(arg[2:])

        if (bookcase := self.sql_session.scalars(
            select(Bookcase)
            .where(Bookcase.name == bookcase_name)
        ).one_or_none()) is None:
            print(f'Error: Could not find bookcase with name {bookcase_name}')
            return

        if self.sql_session.scalars(
            select(BookcaseShelf)
            .where(
              BookcaseShelf.bookcase == bookcase,
              BookcaseShelf.row == row,
              BookcaseShelf.column == column,
            )
        ).one_or_none() is not None:
            print(f'Error: a bookshelf in bookcase {bookcase.name} with position {row}-{column} already exists')
            return

        shelf = BookcaseShelf(
            row,
            column,
            bookcase,
            description,
        )
        self.sql_session.add(shelf)


    def do_list_bookcase_items(self, _: str):
        """Usage: list_bookcase_items"""
        self.columnize([repr(bi) for bi in self.bookcase_items])


    def default(self, isbn: str):
        isbn = isbn.strip()
        if not is_valid_isbn(isbn):
            print(f'"{isbn}" is not a valid isbn')
            return

        if (existing_item := self.sql_session.scalars(
            select(BookcaseItem)
            .where(BookcaseItem.isbn == isbn)
        ).one_or_none()) is not None:
            print('Found existing BookcaseItem:', existing_item)
            print(f'There are currently {existing_item.amount} of these in the system.')
            if _prompt_yes_no('Would you like to add another?', default=True):
                existing_item.amount += 1
            return

        bookcase_item = create_bookcase_item_from_isbn(isbn, self.sql_session)
        if bookcase_item is None:
            print(f'Could not find data about item with isbn {isbn} online.')
            print(f'If you think this is not due to a bug, please add the book to openlibrary.org before continuing.')
            return
        else:
            print(dedent(f"""
            Found item:
              title: {bookcase_item.name}
              authors: {', '.join(a.name for a in bookcase_item.authors)}
              language: {bookcase_item.language}
            """))

        print('Please select the shelf where the item is placed:')
        bookcase_shelf_selector = _InteractiveItemSelector(
            cls = BookcaseShelf,
            sql_session = self.sql_session,
        )

        bookcase_shelf_selector.cmdloop()
        bookcase_item.shelf = bookcase_shelf_selector.result

        print('Please select the items media type:')
        media_type_selector = _InteractiveItemSelector(
            cls = MediaType,
            sql_session = self.sql_session,
            default = self.sql_session.scalars(
              select(MediaType)
              .where(MediaType.name.ilike("book")),
            ).one(),
        )

        media_type_selector.cmdloop()
        bookcase_item.media_type = media_type_selector.result

        username = input('Who owns this book? [PVV]: ')
        if username != '':
            bookcase_item.owner = username

        self.sql_session.add(bookcase_item)


    def do_exit(self, _: str):
        """Usage: exit"""
        if _prompt_yes_no('Would you like to save your changes?'):
            self.sql_session.commit()
        else:
            self.sql_session.rollback()
        exit(0)


def main():
    tool = BookScanTool()
    while True:
        try:
            tool.cmdloop()
        except KeyboardInterrupt:
            try:
              print()
              if _prompt_yes_no('Are you sure you want to exit without saving?', default=False):
                  raise KeyboardInterrupt
            except KeyboardInterrupt:
                if tool.sql_session is not None:
                    tool.sql_session.rollback()
                exit(0)

if __name__ == '__main__':
    main()