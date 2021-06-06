from app.models import Todos
from flask import app, request, make_response, redirect, render_template, session, url_for, flash
import unittest
from flask_login import login_required, current_user
from app import create_app
from app.forms import LoginForm
from app.models import Todos
app = create_app()



@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    id_user = session.get('id_user')
    todos_user = Todos.query.filter_by(id_user=id_user).all()

    context = {
        'user_ip' : user_ip,
        'id_user' : id_user,
        'todos' : todos_user,
        'username' : username
        
    }


    return render_template('hello.html', **context)