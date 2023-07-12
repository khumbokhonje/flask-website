import json
from flask_sqlalchemy.pagination import Pagination
from .models import Notes, User
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from . import notesdb

notes = Blueprint('notes', __name__)

@notes.route('', methods=['GET', 'POST'])
@login_required
def note_home():
    # page = request.args.get('page', 1, type=int)
    # user_notes = User.query.get('user_name')
    notess = current_user.notes
    notes = notess.query.get('text_data')
    print(notes)
    # notess = user_notes.query.paginate(page=page, per_page=5)
    # print(notess)  
    if request.method == 'POST':
        note = request.form.get('text-data')
        title = request.form.get('title')
        categ = request.form.get('cats')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Notes(text_data=note, title=title, user_id=current_user.id, category=categ)
            notesdb.session.add(new_note)
            notesdb.session.commit()
            flash('Note added!', category='success')

    return render_template('home.html', user = current_user)

@notes.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user), 404

@notes.route('delete-note', methods=['GET', 'POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Notes.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            notesdb.session.delete(note)
            notesdb.session.commit()
            flash('Note Deleted!', category='error')

    return jsonify({})

@notes.route('user-profile')
def user_profile():
    return render_template('user-profile.html', user=current_user)

@notes.route('delete-account', methods=['GET', 'POST'])
def delete_account():
    user = current_user
    notesdb.session.delete(user)
    notesdb.session.commit()
    return redirect(url_for('notes_auth.notes_login'))
    