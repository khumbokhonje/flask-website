from . import journaldb
from flask_login import UserMixin
from sqlalchemy.sql import func


class Journal(journaldb.Model):
    id = journaldb.Column(journaldb.Integer, primary_key=True)
    data = journaldb.Column(journaldb.String(10000))
    date = journaldb.Column(journaldb.DateTime(timezone=True), default=func.now())
    user_id = journaldb.Column(journaldb.Integer, journaldb.ForeignKey('user.id'))


class User(journaldb.Model, UserMixin):
    id = journaldb.Column(journaldb.Integer, primary_key=True)
    email = journaldb.Column(journaldb.String(150), unique=True)
    password = journaldb.Column(journaldb.String(150))
    first_name = journaldb.Column(journaldb.String(150))
    notes = journaldb.relationship('Note')