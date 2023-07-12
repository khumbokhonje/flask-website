from .models import User
from . import notesdb
from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

notes_auth = Blueprint('notes_auth', __name__)

@notes_auth.route('/login', methods=['GET', 'POST'])
def notes_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(user_email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('notes.note_home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email account does not exist', category='error')

    return render_template('login.html', user=current_user)

@notes_auth.route('/logout')
@login_required
def notes_logout():
    logout_user()
    return redirect(url_for('notes_auth.notes_login'))

@notes_auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email too short', category='error')
        elif len(user_name) < 2:
            flash('Username is too short', category='error')
        elif len(first_name) < 2:
            flash('Name too short', category='error')
        elif len(last_name) < 2:
            flash('Name too short', category='error')
        elif len(password1) < 8:
            flash('Password too short', category='error')
        elif len(password2) < 8:
            flash('Password too short', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            user = User.query.filter_by(user_email=email).first()
            user_nam = User.query.filter_by(user_name=user_name).first()
            if user:
                flash('Email account already registered', category='error')
            else:
                new_user = User(first_name=first_name, user_email=email, user_name=user_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
                notesdb.session.add(new_user)
                notesdb.session.commit()
                login_user(new_user, remember=True)
                return redirect(url_for('notes.note_home'))

    return render_template('sign-up.html', user=current_user)

