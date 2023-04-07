from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.todo_model import Todo

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/users/register', methods = ['POST'])
def user_reg():
    if not User.validator(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' : hashed_pw
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/users/login', methods = ['POST'])
def user_log():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid credentials', 'log')
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid credentials', 'log')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/users/logout')
def log_out():
    del session['user_id']
    # session.clear()
    return redirect('/')

@app.route('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_todos = Todo.get_all()
    return render_template('welcome.html', logged_user = logged_user, all_todos = all_todos)