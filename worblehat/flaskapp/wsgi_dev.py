from werkzeug import run_simple

from worblehat.services.config import Config

from .flaskapp import create_app

def main():
    app = create_app()
    run_simple(
        hostname = 'localhost',
        port = 5000,
        application = app,
        use_debugger = True,
        use_reloader = True,
    )

if __name__ == '__main__':
    main()