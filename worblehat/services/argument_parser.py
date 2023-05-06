from argparse import ArgumentParser
from os import path
from pathlib import Path
from pprint import pformat

def _print_version() -> None:
    from worblehat import __version__
    print(f'Worblehat version {__version__}')


def _is_valid_file(parser: ArgumentParser, arg: str) -> Path:
    path = Path(arg)
    if not path.is_file():
        parser.error(f'The file {arg} does not exist!')

    return path


def parse_args() -> dict[str, any]:
    parser = ArgumentParser(
        description = 'Worblehat library management system',
    )

    parser.add_argument(
        '--verbose',
        action = 'store_true',
        help = 'Enable verbose mode',
    )
    parser.add_argument(
        '--verbose-sql',
        action = 'store_true',
        help = 'Enable verbose SQL mode',
    )
    parser.add_argument(
        '--version',
        action = 'store_true',
        help = 'Print version and exit',
    )
    parser.add_argument(
        '--config',
        type=lambda x: _is_valid_file(parser, x),
        help = 'Path to config file',
        dest = 'config_file',
        metavar = 'FILE',
    )
    parser.add_argument(
        '--print-config',
        action = 'store_true',
        help = 'Print configuration and quit',
    )

    args = parser.parse_args()

    if args.version:
        _print_version()
        exit(0)

    if args.print_config:
        print(f'Configuration:\n{pformat(vars(args))}')
        exit(0)

    return vars(args)
