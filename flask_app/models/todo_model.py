from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model

class Todo:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.due = data['due']
        self.completed = data['completed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# ---------------------CLASSMETHODS-------------------------

    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO todos (title, description, due, completed, user_id)
            VALUES (%(title)s, %(description)s, %(due)s, %(completed)s, %(user_id)s);
        '''
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM todos
            JOIN users ON todos.user_id = users.id;
        '''
        results = connectToMySQL(DATABASE).query_db(query)
        all_todos = []
        if results:
            for row in results:
                this_todo = cls(row)
                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['created_at'],
                    'updated_at' : row['updated_at']
                }
                this_user = user_model.User(user_data)
                this_todo.planner = this_user
                all_todos.append(this_todo)
        return all_todos
    @classmethod
    def get_by_id(cls,data):
        query = '''
            SELECT * FROM todos
            JOIN users ON todos.user_id = users.id
            WHERE todos.id = %(id)s;
        '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            this_todo = cls(results[0])
            row = results[0]
            user_data = {
                **row,
                'id' : row['users.id'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            this_user = user_model.User(user_data)
            this_todo.planner = this_user
            return this_todo
        return False
    @classmethod
    def update(cls, data):
        query = '''
            UPDATE todos SET title = %(title)s, description = %(description)s,
            due = %(due)s, completed = %(completed)s
            WHERE id = %(id)s;
        '''
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def delete(cls, data):
        query = '''
            DELETE FROM todos
            WHERE id = %(id)s;
        '''
        return connectToMySQL(DATABASE).query_db(query, data)

# ---------------------STATICMETHODS-------------------------

    @staticmethod
    def validator(form_data):
        is_valid = True

        if len(form_data['title']) < 1:
            flash('Title is required!')
            is_valid = False

        if len(form_data['description']) < 1:
            flash('Description is required!')
            is_valid = False

        if len(form_data['due']) < 1:
            flash('Due date is required!')
            is_valid = False

        if len(form_data['completed']) < 1:
            flash('Completed date required!')
            is_valid = False
        return is_valid