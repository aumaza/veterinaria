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
# LISTAR DOCTORES
# =======================================================================
@views.route('/doctores')
@login_required
def doctor():
	doctors = User.query.filter_by(user_type="doctor")
	count = User.query.filter_by(user_type="doctor").count()
	return render_template('doctores.html', doctors=doctors, count=count, user=current_user)

# =======================================================================
# LISTAR PROVEEDORES
# =======================================================================
@views.route('/proovedores')
@login_required
def suplier():
	supliers = User.query.filter_by(user_type="proovedor")
	count = User.query.filter_by(user_type="proovedor").count()
	return render_template('proovedores.html', supliers=supliers, count=count, user=current_user)

# =======================================================================
# LISTAR ESPECIES
# =======================================================================
@views.route('/especies')
@login_required
def species():
	animals = Animal.query
	count = Animal.query.count()
	return render_template('especies.html', animals=animals, count=count, user=current_user)

# =======================================================================
# LISTAR RAZAS
# =======================================================================
@views.route('/razas')
@login_required
def races():
	races = Races.query
	count = Races.query.count()
	return render_template('razas.html', races=races, count=count, user=current_user)



# =======================================================================
# FORMULARIO NUEVO REGISTRO DE ESPECIE
# =======================================================================
@views.route('/nueva-especie', methods=['GET', 'POST'])
@login_required
def new_specie():
	if request.method == 'POST':
		especie = request.form.get('especie')

		specie = Animal.query.filter_by(specie=especie).first()

		if specie:
			flash('Especie existente!', category='error')
		elif len(especie) == 0:
			flash('Debe completar el campo!', category='error')
		else:
			new_specie = Animal(specie = especie)
			db.session.add(new_specie)
			db.session.commit()
			flash('Registro Agregado Satisfactoriamente!', category='success')
			return redirect(url_for('views.species'))

	return render_template('nueva-especie.html', user=current_user)


# =======================================================================
# FORMULARIO NUEVO REGISTRO DE ESPECIE
# =======================================================================
@views.route('nueva-raza', methods=['GET', 'POST'])
@login_required
def new_race():
	animals = Animal.query.order_by(Animal.specie.asc())

	if request.method == 'POST':
		specie = request.form.get('specie')
		race = request.form.get('raza')
		raza = Races.query.filter_by(race=race).first()

		if raza:
			flash('Raza ya cargada!', category='error')		
		elif len(specie) == 0 or len(race) == 0:
			flash('Debe seleccionar una Especie o completar el campo raza!', category='error')
		else:
			new_race = Races(specie=specie, race=race)
			db.session.add(new_race)
			db.session.commit()
			flash('Registro agregado exitosamente!', category='success')
			return redirect(url_for('views.races'))

	return render_template('nueva-raza.html', animals=animals, user=current_user)


# =======================================================================
# FORMULARIO EDICION DE DATOS DE USUARIO
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


# =======================================================================
# FORMULARIO DE CAMBIO DE PASSWORD
# =======================================================================
@views.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def user_pass(id):
	usr = User.query.get_or_404(id)

	if request.method == 'POST':
		pass_1 = request.form.get('pwd_1')
		pass_2 = request.form.get('pwd_2')

		if len(pass_1) == 0 or len(pass_2) == 0:
			flash('Debe Completar los campos de Password!', category='error')
		elif pass_1 != pass_2:
			flash('Los Password no coinciden', category='error')
		elif len(pass_1) < 8 or len(pass_2) < 8:
			flash('Los Password No pueden tener menos de 8 caracteres!', category='error')
		else:
			usr.password = generate_password_hash(pass_1, method='sha256')
			db.session.add(usr)
			db.session.commit()
			flash('Su Password se ha actualizado Exitosamente. Ingrese Nuevamente!', category='success')
			return redirect(url_for('auth.login'))

	return render_template('change_password.html', user=current_user)