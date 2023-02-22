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
# LISTAR CLIENTES
# =======================================================================
@views.route('/clientes')
@login_required
def costumer():
	costumers = User.query.filter_by(user_type="cliente")
	count = User.query.filter_by(user_type="cliente").count()
	return render_template('clientes.html', costumers=costumers, count=count, user=current_user)


# =======================================================================
# LISTAR CLIENTES
# =======================================================================
@views.route('/doctores')
@login_required
def doctor():
	doctors = User.query.filter_by(user_type="doctor")
	count = User.query.filter_by(user_type="doctor").count()
	return render_template('doctores.html', doctors=doctors, count=count, user=current_user)

# =======================================================================
# LISTAR CLIENTES
# =======================================================================
@views.route('/proovedores')
@login_required
def suplier():
	supliers = User.query.filter_by(user_type="proovedor")
	count = User.query.filter_by(user_type="proovedor").count()
	return render_template('proovedores.html', supliers=supliers, count=count, user=current_user)

# =======================================================================
# LISTAR CLIENTES
# =======================================================================
@views.route('/especies')
@login_required
def species():
	animals = Animal.query
	count = Animal.query.count()
	return render_template('especies.html', animals=animals, count=count, user=current_user)


# =======================================================================
# EDICION DE DATOS
# =======================================================================
@views.route('/user_bio/<int:id>', methods=['GET', 'POST'])
@login_required
def user_bio(id):
	usr = User.query.get_or_404(id)

	if request.method == 'POST':
		cellphone = request.form.get('cellphone')
		address = request.form.get('address')
		localization = request.form.get('localization')
		user_type = request.form.get('user_type')

		if len(cellphone) == 0 or len(address) == 0 or len(localization) == 0 or len(user_type) == 0:
			flash('Debe completar los campos solicitados!', category='error')
		else:
			usr.cellphone = cellphone
			usr.address = address
			usr.localization = localization
			usr.user_type = user_type
			db.session.add(usr)
			db.session.commit()
			flash('Los datos han sido modificados exitosamente', category='success')
			return redirect(url_for('views.main'))

	return render_template('user_bio.html', usr=usr, user=current_user)