from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True)
    user = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    cellphone =db.Column(db.String(10))
    address = db.Column(db.String(200))
    localization = db.Column(db.String(300))
    password = db.Column(db.String(150))
    user_type = db.Column(db.String(150))
    role = db.Column(db.Integer)

class Animal(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	specie = db.Column(db.String(200), unique=True)

class Races(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	race = db.Column(db.String(500), unique=True)

class Pets(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer)
	doctor_id = db.Column(db.Integer)
	pet_name = db.Column(db.String(100))
	pet_birth = db.Column(db.String(15))
	pet_age = db.Column(db.Integer)
	pet_type = db.Column(db.String(100))
	pet_race = db.Column(db.String(100))
	pet_photo = db.Column(db.String(200))