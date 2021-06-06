from sqlalchemy.orm import backref
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    def __init__(self,  username,  password):
        self.username = username
        self.password = password

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    tasks = db.relationship('Todos', backref="users", lazy=True)

class Todos(db.Model):
    __tablename__ = 'todos'
    def __init__(self, description, id_user):
        self.description = description
        self.id_user = id_user

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(45), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def get_user(username):
    return Users.query.filter_by(username=username).first()

def get_id_user(username):
    active_user = get_user(username)
    return active_user.id


class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserModel(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.username
        self.password = user_data.password
    @staticmethod   
    def query(username):
        user_doc = get_user(username)
        user_data = UserData(
        username=user_doc.username,
        password=user_doc.password,
        )

        return UserModel(user_data) 

