from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True)
    user = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    user_type = db.Column(db.String(150))
    role = db.Column(db.Integer)