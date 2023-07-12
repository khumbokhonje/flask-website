from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


notesdb = SQLAlchemy()
NOTES_DB_NAME = 'note-database.db'

def create_note_app():
    noteapp = Flask(__name__)
    noteapp.config['SECRET_KEY'] = 'jgfhdhshjsjkfdjfh'
    noteapp.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NOTES_DB_NAME}'
    notesdb.init_app(noteapp)

    from .views import notes
    from .auth import notes_auth

    noteapp.register_blueprint(notes_auth, url_prefix='/notes')
    noteapp.register_blueprint(notes, url_prefix='/notes')

    from .models import User, Notes

    create_notes_database(noteapp)

    login_manager = LoginManager()
    login_manager.login_view = 'notes_auth.notes_login'
    login_manager.init_app(noteapp)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return noteapp

def create_notes_database(app):
    if not path.exists('instance/' + NOTES_DB_NAME):
        with app.app_context():
            notesdb.create_all()
            print('Created the notes database!')
