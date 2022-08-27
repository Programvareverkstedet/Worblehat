from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from os import environ, path
from dotenv import load_dotenv

from worblehat.database import db_session, init_db, drop_db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    configure_database(app)
    configure_admin(app)
    configure_blueprints(app)

    @app.route('/')
    def index():
        return 'Hello World!'

    return app


def configure_database(app):
    @app.cli.command("initdb")
    def initdb_command():
        init_db()
        print("Initialized the database.")

    @app.cli.command("resetdb")
    def resetdb_command():
        drop_db()
        print("Cleared the database.")
        init_db()
        from worblehat.models.MediaType import MediaType
        from worblehat.models.Bookcase import Bookcase
        from worblehat.models.Location import Location
        from worblehat.models.Language import Language

        media_types = [
            MediaType(name='Book', description='A physical book'),
            MediaType(name='Comic', description='A comic book'),
            MediaType(name='Video Game', description='A digital game for computers or games consoles'),
            MediaType(name='Tabletop Game', description='A physical game with cards, boards or similar')
        ]

        bookcases = [
            Bookcase(name='A', description='The first bookcase'),
            Bookcase(name='B', description='The second bookcase'),
        ]
        
        locations = [
            Location(name='1-1', description='The first location', bookcase=bookcases[0]),
            Location(name='1-2', description='The second location', bookcase=bookcases[0]),
            Location(name='1-1', description='The first location', bookcase=bookcases[1]),
            Location(name='1-2', description='The second location', bookcase=bookcases[1]),
        ]

        languages = [
            Language(name='English', shortname='en'),
            Language(name='Norwegian', shortname='no'),
            Language(name='Japanese', shortname='ja'),
            Language(name='Swedish', shortname='sv'),
            Language(name='German', shortname='de'),
            Language(name='Russian', shortname='ru'),
            Language(name='Danish', shortname='da')
        ]

        db_session.add_all(media_types)
        db_session.add_all(bookcases)
        db_session.add_all(locations)
        db_session.add_all(languages)
        db_session.commit()
        print("Added media types, bookcases and locations.")



    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

def configure_admin(app):
    admin = Admin(app, name='Worblehat', template_mode='bootstrap3')
    
    from worblehat.models.Category import Category
    from worblehat.models.Item import Item
    from worblehat.models.MediaType import MediaType
    from worblehat.models.Location import Location
    from worblehat.models.Bookcase import Bookcase

    admin.add_view(ModelView(Category, db_session))
    admin.add_view(ModelView(Item, db_session))
    admin.add_view(ModelView(MediaType, db_session))
    admin.add_view(ModelView(Location, db_session))
    admin.add_view(ModelView(Bookcase, db_session))

def configure_blueprints(app):
    from worblehat.blueprints.main import main
    blueprints = [main]

    for bp in blueprints:
        app.register_blueprint(bp)