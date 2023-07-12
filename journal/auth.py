from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import journaldb
from flask_login import login_user, login_required, logout_user, current_user

journal_auth = Blueprint('auth', __name__)

@journal_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email does not exist!', category='error')

    return render_template('login.html', user=current_user)

@journal_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@journal_auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')

        elif len(email) < 4:
            flash('Email must be greater than four characters', category='error')
        elif len(firstName) < 2:
            flash('Firstname must be greater than one character', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password too short', category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
            journaldb.session.add(new_user)
            journaldb.session.commit()
            flash('Account logged in', category='success')
            login_user(user, remember=True, force=True)
            return redirect(url_for('views.home'))

            
    return render_template('sign-up.html', user=current_user)