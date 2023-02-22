from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from markupsafe import escape
from os.path import join, dirname, realpath
from datetime import datetime
import imghdr
import os
from . import db
import json
import shutil


views = Blueprint('views', '__name__')
from .models import User, Animal, Races, Pets

@views.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)


@views.route('/main')
@login_required
def main():
    return render_template('main.html', user=current_user)



# =======================================================================
# EDICION DE DATOS
# =======================================================================
@views.route('/user_bio/<int:id>', methods=['GET', 'POST'])
@login_required
def user_bio(id):
	usr = User.query.get_or_404(id)

	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')

		if len(name) == 0 or len(email) == 0:
			flash('Debe completar los campos!', category='error')
		elif name == usr.name and email == usr.email:
			flash('Los datos no serán modificados. Ambos son iguales a los ya registrados!', category='error')
		else:
			usr.name = name
			usr.user = email
			usr.email = email
			db.session.add(usr)
			db.session.commit()
			flash('Los datos han sido modificados exitosamente', category='success')
			return redirect(url_for('auth.logout'))

	return render_template('user_bio.html', usr=usr, user=current_user)