from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user_model import User
from flask_app.models.todo_model import Todo



@app.route('/todos/new')
def new_todo():
    return render_template('todo_new.html')


@app.route('/todos/create', methods = ['POST'])
def create_todo():
    if 'user_id' not in session:
        return('/')
    if not Todo.validator(request.form):
        return redirect('/todos/new')
    todo_data = {
        **request.form,
        'user_id' : session['user_id']
    }
    Todo.create(todo_data)
    return redirect('/dashboard')


@app.route('/todos/<int:id>')
def show_one_todo(id):
    if 'user_id' not in session:
        return('/')
    this_todo = Todo.get_by_id({'id' : id})
    logged_user = User.get_by_id({'id' : session['user_id']})
    return render_template('todo_one.html', this_todo = this_todo, logged_user = logged_user)


@app.route('/todos/<int:id>/edit')
def edit_user_todo(id):
    if 'user_id' not in session:
        return('/')
    data = {
        'id' : id
    }
    one_todo = Todo.get_by_id(data)

    if not one_todo.user_id == session['user_id']: #                      extra
        flash('You are not original owner of todo. Cannot edit!')
        return redirect('/dashboard')

    return render_template('todo_edit.html', one_todo = one_todo)


@app.route('/todos/<int:id>/update', methods = ['POST'])
def update_user(id):
    if 'user_id' not in session:
        return('/')

    if not Todo.validator(request.form):
        return redirect(f'/todos/{id}/edit')

    data = {
        'id' : id,
        **request.form
    }
    todo_to_update = Todo.get_by_id(data)

    if not todo_to_update.user_id == session['user_id']: #                extra
        flash('Unauthorized user! Cannot update!')
        return redirect('/dashboard')

    Todo.update(data)
    return redirect('/dashboard')


@app.route('/todos/<int:id>/delete')
def del_todo(id):
    if 'user_id' not in session:
        return('/')
    data = {
        'id' : id,
    }
    this_todo = Todo.get_by_id(data)

    if not this_todo.user_id == session['user_id']: #                     extra
        flash('Unauthorized user! Cannot delete!')
        return redirect('/dashboard')
    
    Todo.delete(data)
    return redirect('/dashboard')