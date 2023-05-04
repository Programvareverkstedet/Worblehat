from cmd import Cmd
from typing import Any, Set

from sqlalchemy import (
   create_engine,
   select,
)
from sqlalchemy.orm import (
   Session,
)

from worblehat.services.item import (
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
        items: Set[Any],
        default: Any | None = None,
    ):
        super().__init__()
        self.cls = cls
        self.sql_session = sql_session
        self.items = items
        self.default_item = default
        if default is not None:
          self.prompt = f'Select {cls.__name__} [{default.name}]> '
        else:
          self.prompt = f'Select {cls.__name__}> '

    def default(self, arg: str):
        if arg == '' and self.default_item is not None:
            self.result = self.default_item
            return True

        if self.sql_session is not None:
            result = self.sql_session.scalars(
                select(self.cls)
                .where(self.cls.name == arg),
            ).all()
        else:
            result = [x for x in self.items if x.name == arg]

        if len(result) != 1:
            print(f'No such {self.cls.__name__} found: {arg}')
            return

        self.result = result[0]
        return True

    def completenames(self, text: str, *_) -> list[str]:
        if self.sql_session is not None:
            return self.sql_session.scalars(
                select(self.cls.name)
                .where(self.cls.name.like(f'{text}%'))
            ).all()
        else:
            return [x for x in self.items if x.name.startswith(text)]


class BookScanTool(Cmd):
    prompt = '> '
    intro = """
Welcome to the worblehat scanner tool.
Start by entering a command, or entering an ISBN of a new item.
Type "help" to see list of commands
    """

    sql_session = None

    bookcases: set[Bookcase] = set()
    bookcase_locations: set[BookcaseLocation] = set()
    bookcase_items: set[BookcaseItem] = set()
    media_types: set[MediaType] = set()

    def __init__(self):
        super().__init__()

        try:
            engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
            self.sql_session = Session(engine)
        except Exception:
            print('Warning: could not connect to database. Saving to database has been disabled.')
            return

        try:
             self.bookcases = set(self.sql_session.scalars(select(Bookcase)).all())
             self.bookcase_locations = set(self.sql_session.scalars(select(BookcaseLocation)).all())
             self.bookcase_items = set(self.sql_session.scalars(select(BookcaseItem)).all())
             self.media_types = set(self.sql_session.scalars(select(MediaType)).all())
        except Exception as e:
            print(e)
            print('Warning: could not prefill data from sql database. Saving to database has been disabled.')
            self.sql_session.close()
            self.sql_session = None
            return

        print('Note: Successfully connected to database')


    def do_list_bookcases(self, arg: str):
        self.columnize([repr(bc) for bc in self.bookcases])


    def do_add_bookcase(self, arg: str):
        """
        Usage: add_bookcase <name> [description]
        """
        arg = arg.split(' ')
        if len(arg) < 1:
            print('Usage: add_bookcase <name> [description]')
            return

        name = arg[0]
        description = ' '.join(arg[1:])

        if any([bc.name == name for bc in self.bookcases]):
            print(f'Error: a bookcase with name {name} already exists')
            return

        bookcase = Bookcase(name, description)
        self.bookcases.add(bookcase)
        if self.sql_session is not None:
            self.sql_session.add(bookcase)


    def do_list_bookcase_locations(self, arg: str):
        self.columnize([repr(bl) for bl in self.bookcase_locations])


    def do_add_bookcase_location(self, arg: str):
        """
        Usage: add_bookcase_location <bookcase_name> <name> [description]
        """
        arg = arg.split(' ')
        if len(arg) < 2:
            print('Usage: add_bookcase_location <bookcase_name> <name> [description]')
            return

        bookcase_name = arg[0]
        name = arg[1]
        description = ' '.join(arg[2:])

        bookcases_with_name = [bc for bc in self.bookcases if bc.name == bookcase_name]
        if not len(bookcases_with_name) == 1:
            print(f'Error: Could not find bookcase with name {bookcase_name}')
            return

        if any([bc.name == name for bc in self.bookcase_locations]):
            print(f'Error: a bookcase with name {name} already exists')
            return

        location = BookcaseLocation(
            name,
            bookcases_with_name[0],
            description,
        )
        self.bookcase_locations.add(location)
        if self.sql_session is not None:
            self.sql_session.add(location)


    def do_list_bookcase_items(self, arg: str):
        self.columnize([repr(bi) for bi in self.bookcase_items])


    def default(self, arg: str):
        if not is_valid_isbn(arg):
            print(f'"{arg}" is not a valid isbn')
            return

        bookcase_item = create_bookcase_item_from_isbn(arg)
        if bookcase_item == None:
            print(f'Could not find data about item with isbn {arg} online.')
            print(f'If you think this is not due to a bug, please add the book to openlibrary.org before continuing.')

        print('Please select the location where the item is placed:')
        bookcase_location_selector = _InteractiveItemSelector(
            cls = BookcaseLocation,
            sql_session = self.sql_session,
            items = self.bookcase_locations,
        )

        bookcase_location_selector.cmdloop()
        bookcase_item.location = bookcase_location_selector.result

        print('Please select the items media type:')
        media_type_selector = _InteractiveItemSelector(
            cls = MediaType,
            sql_session = self.sql_session,
            items = self.media_types,
            default = next(mt for mt in self.media_types if mt.name.lower() == 'book'),
        )

        media_type_selector.cmdloop()
        bookcase_item.media_type = media_type_selector.result

        username = input('Who owns this book? [PVV]: ')
        if username != '':
            bookcase_item.owner = username

        self.bookcase_items.add(bookcase_item)
        if self.sql_session is not None:
            self.sql_session.add(bookcase_item)


    def do_exit(self, arg: str):
        # TODO: take internally stored data, and save it, either in csv, json or database
        raise NotImplementedError()


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