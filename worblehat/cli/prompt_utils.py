from cmd import Cmd
from typing import Any, Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

def prompt_yes_no(question: str, default: bool | None = None) -> bool:
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


class InteractiveItemSelector(Cmd):
    def __init__(
        self,
        cls: type,
        sql_session: Session,
        execute_selection: Callable[[Session, type, str], list[Any]] = lambda session, cls, arg: session.scalars(
            select(cls)
            .where(cls.name == arg),
        ).all(),
        complete_selection: Callable[[Session, type, str], list[str]] = lambda session, cls, text: session.scalars(
            select(cls.name)
            .where(cls.name.ilike(f'{text}%')),
        ).all(),
        default: Any | None = None,
    ):
        """
        This is a utility class for prompting the user to select an
        item from the database. The default functions assumes that
        the item has a name attribute, and that the name is unique.
        However, this can be overridden by passing in custom functions.
        """

        super().__init__()

        self.cls = cls
        self.sql_session = sql_session
        self.execute_selection = execute_selection
        self.complete_selection = complete_selection
        self.default_item = default

        if default is not None:
          self.prompt = f'Select {cls.__name__} [{default.name}]> '
        else:
          self.prompt = f'Select {cls.__name__}> '


    def emptyline(self) -> bool:
        if self.default_item is not None:
            self.result = self.default_item
            return True


    def default(self, arg: str):
        result = self.execute_selection(self.sql_session, self.cls, arg)

        if len(result) != 1:
            print(f'No such {self.cls.__name__} found: {arg}')
            return

        self.result = result[0]
        return True

    # TODO: Override this function to not act as an argument completer
    #       but to complete the entire value name
    def completedefault(self, text: str, line: str, *_) -> list[str]:
        return []

    def completenames(self, text: str, *_) -> list[str]:
        x = self.complete_selection(self.sql_session, self.cls, text)
        return x


class NumberedCmd(Cmd):
    """
    This is a utility class for creating a numbered command line.

    It will automatically generate a prompt that lists all the
    available commands, and will automatically call the correct
    function based on the user input.

    If the user input is not a number, it will call the default
    function, which can be overridden by the subclass.

    Example:
    ```
    class MyCmd(NumberedCmd):
        def __init__(self):
            super().__init__()

        def do_foo(self, arg: str):
            pass

        def do_bar(self, arg: str):
            pass

        funcs = {
            1: {
                'f': do_foo,
                'doc': 'do foo',
            },
            2: {
                'f': do_bar,
                'doc': 'do bar',
            },
        }
    ```
    """


    prompt_header: str | None = None


    def __init__(self):
        super().__init__()


    @classmethod
    def _generate_usage_list(cls) -> str:
        result = ''
        for i, func in cls.funcs.items():
            if i == 0:
                i = '*'
            result += f'{i}) {func["doc"]}\n'
        return result


    def _default(self, arg: str):
        try:
            i = int(arg)
            self.funcs[i]
        except (ValueError, KeyError):
            return

        self.funcs[i]['f'](self, arg)


    def default(self, arg: str):
        self._default(arg)


    def _postcmd(self, stop: bool, line: str) -> bool:
        print()
        print('-----------------')
        print()
        return stop


    def postcmd(self, stop: bool, line: str) -> bool:
        return self._postcmd(stop, line)


    @property
    def prompt(self):
        result = ''

        if self.prompt_header != None:
            result += self.prompt_header + '\n'

        result += self._generate_usage_list()

        if self.lastcmd == '':
            result += f'> '
        else:
            result += f'[{self.lastcmd}]> '

        return result