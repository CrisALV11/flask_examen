from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User, Products
from . import user_datastore, db

client = Blueprint('client', __name__, url_prefix='/client')

@client.route("/consult", methods=["GET", "POST"])
@login_required
@roles_required('client')
def consult():
    product = Products.query.all()
    return render_template("",  products = product)
