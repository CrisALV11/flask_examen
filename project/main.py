from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from .models import User
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
@roles_required('admin')
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/login', methods=['POST', 'GET'])
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
            return redirect(url_for('main.login'))

        # Se autentica a el usuario
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    return render_template('/security/login.html')


@main.route('/logout')
@login_required
def logout():
    # Cerrar sesión
    logout_user()
    return redirect(url_for('main.index'))


