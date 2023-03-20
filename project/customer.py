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
    products = Products.query.filter(Products.active == 1).all()
    page = request.args.get('page', 1, type=int)
    per_page = 6
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_articles = products[start_idx:end_idx]
    num_pages = len(products) // per_page + (len(products) % per_page > 0)

    return render_template('gallery.html', articles=page_articles, num_pages=num_pages, current_page=page)
