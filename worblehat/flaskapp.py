from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import inspect

from .database import db
from .models import *
from .config import Config

from .blueprints.main import main
from .seed_test_data import seed_data

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        if not inspect(db.engine).has_table('Bookcase'):
            Base.metadata.create_all(db.engine)
            seed_data(db)

    configure_admin(app)

    app.register_blueprint(main)

    return app

def configure_admin(app):
    admin = Admin(app, name='Worblehat', template_mode='bootstrap3')
    admin.add_view(ModelView(Author, db.session))
    admin.add_view(ModelView(Bookcase, db.session))
    admin.add_view(ModelView(BookcaseItem, db.session))
    admin.add_view(ModelView(BookcaseLocation, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Language, db.session))
    admin.add_view(ModelView(MediaType, db.session))