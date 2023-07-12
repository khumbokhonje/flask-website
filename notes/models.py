from . import notesdb
from sqlalchemy.sql import func
from flask_login import UserMixin

class Notes(notesdb.Model):
    id = notesdb.Column(notesdb.Integer, primary_key=True)
    title = notesdb.Column(notesdb.String(100))
    text_data = notesdb.Column(notesdb.String(10000))
    date = notesdb.Column(notesdb.DateTime(timezone=True), default=func.now())
    user_id = notesdb.Column(notesdb.Integer, notesdb.ForeignKey('user.id'))
    category = notesdb.Column(notesdb.String(50), default='My Notes')

class User(notesdb.Model, UserMixin):
    id = notesdb.Column(notesdb.Integer, primary_key=True)
    first_name = notesdb.Column(notesdb.String(100))
    last_name = notesdb.Column(notesdb.String(100))
    user_name = notesdb.Column(notesdb.String(1000))
    password = notesdb.Column(notesdb.String(100))
    user_email = notesdb.Column(notesdb.String(100))
    notes = notesdb.relationship('Notes')