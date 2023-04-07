from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import todo_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.firstname = data['first_name']
        self.lastname = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# ---------------------CLASSMETHODS-------------------------

    @classmethod
    def create(cls,data):
        query = '''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        '''
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_by_email(cls,data):
        query = '''
            SELECT * FROM users
            WHERE email = %(email)s;
        '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = '''
            SELECT * FROM users
            LEFT JOIN todos ON users.id = todos.user_id
            WHERE users.id = %(id)s;
        '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            todo_list = []
            this_user = cls(results[0])
            for row in results:
                todo_data = {
                    **row,
                    'id' : row['todos.id'],
                    'created_at' : row['todos.created_at'],
                    'updated_at' : row['todos.updated_at']
                }
                this_todo_instance = todo_model.Todo(todo_data)
                todo_list.append(this_todo_instance)
            this_user.todos = todo_list
            return this_user
        return False

# ---------------------CLASSMETHODS-------------------------

    @staticmethod
    def validator(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash('First Name Required', 'reg')
            is_valid = False

        if len(data['last_name']) < 1:
            flash('Last Name Required', 'reg')
            is_valid = False

        if len(data['email']) < 1:
            flash('E-mail Name Required', 'reg')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash('Invalid E-mail', 'reg')
            is_valid = False
        else:
            user_data = {
                'email' : data['email']
            }
            potential_user = User.get_by_email(user_data)
            if potential_user:
                flash('E-mail already exists', 'reg')
                is_valid = False

        if len(data['password']) < 1:
            flash('Password Required', 'reg')
            is_valid = False
        elif not data['password'] == data['confirm_pw']:
            flash('Please double check that passwords match.', 'reg')
            is_valid = False
        return is_valid