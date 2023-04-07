from flask import Flask
app = Flask(__name__)
app.secret_key = 'pineapple chunks'

DATABASE = 'mydb'