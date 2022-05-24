from unicodedata import category
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db
from flask_login import login_user, logout_user, login_required, current_user
from models.Usermodel import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You are logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='danger')
                return redirect(url_for('auth.login'))
        else:
            flash('You are not registered!', category='danger')
            return redirect(url_for('auth.signup'))
    return render_template('login.html', user = current_user)

@auth.route('/myprofile', methods=["GET", "POST"])
@login_required
def myprofile():
    return 'my profile'


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash ('You are logged out', category='success')
    return redirect(url_for('auth.login'))



@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password= request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='danger')
            return redirect(url_for('auth.login'))
        elif password!= password2:
            flash('Passwords don\'t match.', category='danger')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='danger')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 character.', category='danger')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='danger')
        else:
        
            new_user = User(email=email, firstname=firstname, password=generate_password_hash(
                password, method='sha256'))

            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html", user = current_user)


