from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User
from . import user_datastore, db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/profile')
@login_required
@roles_required('admin')
def profile():
    return render_template('profile.html', name=current_user.name)