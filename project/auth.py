from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User
from . import user_datastore, db

auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        # Verifica si hay un usuario creado con el email
        user  = User.query.filter_by(email=email).first()

        # Verifica si el usuario existe
        if not user or not check_password_hash(user.password, password):
            flash('El usuario y/o contraseña son incorrectos')
            return redirect(url_for('auth.login'))

        # Se autentica a el usuario
        login_user(user, remember=remember)
        return redirect(url_for('customer.gallery'))
    return render_template('/security/login.html')

@auth.route('/register',  methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # Verifica si el correo ya existe
        if user:
            flash('El correo electrónico ya está registrado')
            return redirect(url_for('auth.register'))

        # Se crea un nuevo usuario con los datos del formulario
        # Se realiza un hash a la contraseña
        user_datastore.create_user(name=name, email=email, 
                                   password=generate_password_hash(password, method='sha256'),
                                   active = True)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('/security/register.html')

@auth.route('/logout')
@login_required
def logout():
    # Cerrar sesión
    logout_user()
    return redirect(url_for('main.index'))