from flask import render_template, session, redirect, url_for, flash
import flask_login
from flask_login import login_user, logout_user

from app.forms import LoginForm

from . import auth

from app.models import UserData, get_user, UserModel



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
            password_db = user_doc.password

            if password == password_db:
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