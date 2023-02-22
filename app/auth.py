from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', '__name__')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = request.form.get('user')
		password = request.form.get('pwd')

		user = User.query.filter_by(user=user).first()

		if user == "" or password == "":
			flash('Debe ingresar sus datos!', category='error')
		elif user:
			if check_password_hash(user.password, password):
				if(user.role == 1):
					flash('Bienvenido/a %s' % (user.name), category='success')
					login_user(user, remember=False)
					return redirect(url_for('views.main'))
				elif user.role == 0:
					flash('Usuario Bloqueado. Cantacte al Administrador!', category='error')

			else:
				flash('El usuario o el password es incorrecto!', category='error')

	return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Ha salido del sistema satisfactoriamente', category='success')
	return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		user_type = request.form.get('user_type')
		cellphone = request.form.get('cellphone')
		address = request.form.get('address')
		localization = request.form.get('localization')	
		pass_1 = request.form.get('pwd_1')
		pass_2 = request.form.get('pwd_2')
		
		user = User.query.filter_by(user=email).first()

		if user:
			flash('Usuario existente', category='error')
		elif len(email) == 0:
			flash('Debe Ingresar un Email', category='error')
		elif len(name) == 0:
			flash('Debe ingresar su Nombre', category='error')
		elif len(user_type) == 0:
			flash('Debe seleccionar un tipo de usuario', category='error')
		elif len(cellphone) == 0:
			flash('Debe ingresar el número de celular', category='error')
		elif len(address) == 0:
			flash('Debe ingresar su dirección!', category='error')
		elif len(localization) == 0:
			flash('Debe ingresar una localidad!', category='error')
		elif pass_1 != pass_2:
			flash('Los Passwords no coinciden. Reintente', category='error')
		elif len(pass_1) < 8:
			flash('El Password no puede ser menor a 8 caracteres', category='error')
		else:
			new_user = User(name=name, user=email, email=email, cellphone=cellphone, address=address, localization=localization, user_type=user_type, password=generate_password_hash(pass_1, method='sha256'), role=1)
			db.session.add(new_user)
			db.session.commit()
			#login_user(user, remember=True)
			flash('Se ha creado el usuario satisfactoriamente!', category='success')
			return redirect(url_for('views.home'))

	return render_template('sign_up.html', user=current_user)


@auth.route('/password', methods=['GET', 'POST'])
def password():
	if request.method == 'POST':
		email = request.form.get('email')
		pass_1 = request.form.get('pwd_1')
		pass_2 = request.form.get('pwd_2')

		user = User.query.filter_by(user=email).first()

		if user:
			if len(pass_1) < 8 or len(pass_2) < 8:
				flash('El password no puede tener menos de 8 Caracteres!', category='error')
			elif pass_1 != pass_2:
				flash('Los Password no coinciden!', category='error')
			else:
				user.password = generate_password_hash(pass_1, method='sha256')
				db.session.add(user)
				db.session.commit()
				flash('Su Password se ha actualizado Exitosamente!', category='success')
				return redirect(url_for('auth.login'))
		else:
			flash('Usuario Inexistente. Antes debe Registrarse!', category='error')

	return render_template('password.html', user=current_user)
