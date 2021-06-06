from enum import auto
from flask import render_template, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app.forms import LoginForm

from . import auth

from app.models import db, UserData, get_user, UserModel, Users



@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form' : LoginForm()
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc is not None:
            if check_password_hash(user_doc['password'], password):
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de nuevo')

                redirect(url_for('hello'))
            else:
                flash('La informacion no coincide')

        else: 
            flash('El usuario no existe')

        return redirect(url_for('index'))

    return render_template('login.html', **context)

@auth.route('logout')
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form

    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = Users.query.filter_by(username=username).first()

        if user_doc:
            flash('Nombre de usuario existente')
            return redirect(url_for('auth.signup'))

        else:
            new_user = Users(username=username, password=generate_password_hash(password, method='sha256'))

            db.session.add(new_user)
            db.session.commit()

            user_data = UserData(username, password)

            user = UserModel(user_data)

            login_user(user)

            flash('Bienvenido!')

            return redirect(url_for('hello'))

    return render_template('signup.html', **context)
