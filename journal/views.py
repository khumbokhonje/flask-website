from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Journal
from . import journaldb
import json

journal = Blueprint('journal', __name__)

@journal.route('/journal', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('text-data')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Journal(data=note, user_id=current_user.id)
            journaldb.session.add(new_note)
            journaldb.session.commit()
            flash('Note added!', category='success')

    return render_template('home.html', user=current_user)

@journal.route('/delete-note', methods=['GET', 'POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Journal.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            journaldb.session.delete(note)
            journaldb.session.commit()

    return jsonify({})