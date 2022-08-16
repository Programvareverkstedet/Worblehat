from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from os import environ, path
from dotenv import load_dotenv

from worblehat.database import db_session, init_db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    configure_database(app)
    configure_admin(app)

    @app.route('/')
    def index():
        return 'Hello World!'

    return app


def configure_database(app):
    @app.cli.command("initdb")
    def initdb_command():
        init_db()
        print("Initialized the database.")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

def configure_admin(app):
    admin = Admin(app, name='Worblehat', template_mode='bootstrap3')
    
    from worblehat.models.Category import Category
    from worblehat.models.Item import Item
    from worblehat.models.MediaType import MediaType

    admin.add_view(ModelView(Category, db_session))
    admin.add_view(ModelView(Item, db_session))
    admin.add_view(ModelView(MediaType, db_session))

