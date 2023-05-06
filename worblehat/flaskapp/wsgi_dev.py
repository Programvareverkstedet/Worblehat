from werkzeug import run_simple

from worblehat.services.config import Config
from worblehat.services.argument_parser import parse_args

from .flaskapp import create_app

def main():
    args = parse_args()
    app = create_app(args)
    run_simple(
        hostname = 'localhost',
        port = 5000,
        application = app,
        use_debugger = True,
        use_reloader = True,
    )

if __name__ == '__main__':
    main()