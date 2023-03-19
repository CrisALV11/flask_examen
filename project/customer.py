from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User, Products
from . import user_datastore, db

customer = Blueprint('customer', __name__, url_prefix='/customer')

@customer.route("/gallery", methods=["GET", "POST"])
@login_required
def gallery():
    product = Products.query.filter(Products.active == 1).all()
    return render_template("gallery.html", products= product)
