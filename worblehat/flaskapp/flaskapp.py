from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import inspect

from worblehat.models import *
from worblehat.services.seed_test_data import seed_data
from worblehat.services.config import Config

from .blueprints.main import main
from .database import db

def create_app(args: dict[str, any] | None = None):
    app = Flask(__name__)

    if args is not None:
        Config.load_configuration(args)
        print(Config.db_string())
        app.config.update(Config['flask'])
        app.config.update(Config._config)
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.db_string()
        app.config['SQLALCHEMY_ECHO'] = args.get('verbose_sql')

    db.init_app(app)

    with app.app_context():
        if not inspect(db.engine).has_table('Bookcase'):
            Base.metadata.create_all(db.engine)
            seed_data()

    configure_admin(app)

    app.register_blueprint(main)

    return app

def configure_admin(app):
    admin = Admin(app, name='Worblehat', template_mode='bootstrap3')
    admin.add_view(ModelView(Author, db.session))
    admin.add_view(ModelView(Bookcase, db.session))
    admin.add_view(ModelView(BookcaseItem, db.session))
    admin.add_view(ModelView(BookcaseShelf, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Language, db.session))
    admin.add_view(ModelView(MediaType, db.session))