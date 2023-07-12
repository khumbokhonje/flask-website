from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

journaldb = SQLAlchemy()
DB_NAME = 'journal_database.db'

def create_app():
    journalapp = Flask(__name__)
    journalapp.config["SECRET_KEY"] = "gfgefsdgfuirfg"
    journalapp.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    journaldb.init_app(journalapp)

    from .views import journal
    from .auth import journal_auth

    journalapp.register_blueprint(journal, url_prefix='/journal')
    journalapp.register_blueprint(journal_auth, url_prefix='/journal')
    
    from .models import User, Journal

    create_database(journalapp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(journalapp)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return journalapp

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            journaldb.create_all()
            print('Created Database!')