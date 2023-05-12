from argparse import ArgumentParser
from pathlib import Path

def _is_valid_file(parser: ArgumentParser, arg: str) -> Path:
    path = Path(arg)
    if not path.is_file():
        parser.error(f'The file {arg} does not exist!')

    return path


arg_parser = ArgumentParser(
    description = 'Worblehat library management system',
)

subparsers = arg_parser.add_subparsers(dest='command')
subparsers.add_parser(
    'cli',
    help = 'Start the command line interface',
)
subparsers.add_parser(
    'flask-dev',
    help = 'Start the web interface in development mode',
)
subparsers.add_parser(
    'flask-prod',
    help = 'Start the web interface in production mode',
)

arg_parser.add_argument(
    '-V',
    '--version',
    action = 'store_true',
    help = 'Print version and exit',
)
arg_parser.add_argument(
    '-c',
    '--config',
    type=lambda x: _is_valid_file(arg_parser, x),
    help = 'Path to config file',
    dest = 'config_file',
    metavar = 'FILE',
)
arg_parser.add_argument(
    '-p',
    '--print-config',
    action = 'store_true',
    help = 'Print configuration and quit',
)
