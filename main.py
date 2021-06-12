from flask_login.utils import login_user
from app.models import Todos
from flask import app, request, make_response, redirect, render_template, session, url_for, flash
import unittest
from flask_login import login_required, current_user
from app import create_app
from app.forms import TodoForm , DeleteTodoForm
from app.models import Todos, db,  get_id_user

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


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    id_user = get_id_user(username)
    todos_user = Todos.query.filter_by(id_user=id_user).all()
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()

    context = {
        'user_ip' : user_ip,
        'id_user' : id_user,
        'todos' : todos_user,
        'username' : username,
        'todo_form' : todo_form,
        'delete_form': delete_form,
        
    }

    if todo_form.validate_on_submit():
        description = todo_form.description.data
        new_todo = Todos(description=description, done=False,  id_user=id_user)

        db.session.add(new_todo)
        db.session.commit()

        flash('Tu tarea se creó con éxito')

        return redirect(url_for('hello'))


    return render_template('hello.html', **context)

@app.route('/todos/delete/<todo_id>', methods=['GET', 'POST'])
def delete(todo_id):

    todo_del = Todos.query.filter_by(todo_id=todo_id).first()
    
    if todo_del is not None:

        db.session.delete(todo_del)
        db.session.commit()
    
    flash("A task was deleted!", "success")
    
    return redirect(url_for('hello'))