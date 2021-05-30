from sqlalchemy.orm import backref
import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    def __init__(self, id, username, name,  password):
        self.id = id
        self.username = username
        self.name = name
        self.password = password

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    password = db.Columnn(db.String(45), nullable=False)
    tasks = db.relationship('Todos', backref="users", lazy=True)

class Todos(db.Model):
    __tablename__ = 'todos'
    def __init__(self, id, description, status, id_users):
        self.id = id
        self.description = description
        self.status = status
        self.id_users = id_users

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(45), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    id_users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    