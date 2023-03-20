from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User, Products
from . import user_datastore, db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route("/consult", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def consult():
    product = Products.query.filter(Products.active == 1).all()
    return render_template("products.html",  products = product)

@admin.route("/register", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def register():
        if request.method == "POST":
        
            product = Products(name = request.form.get('name'),
                            describe =  request.form.get('describe'),
                            active = 1,
                            cost = request.form.get('cost'),
                            photo = request.form.get('photo')
                            )
            db.session.add(product)
            db.session.commit()
            flash('El producto fue agregado con exitó')
            return redirect(url_for('admin.consult'))
        return render_template("register.html")

@admin.route("/update", methods=["GET", "POST"])
@roles_required('admin')
def update():
    if request.method == 'GET':
        id = request.args.get('id')
        product = db.session.query(Products).filter(Products.id == id).first()
        name = product.name
        describe = product.describe
        active = product.active
        cost = product.cost
        photo = product.photo
        dicProducto = {
            "id": id,
            "name": name,
            "describe": describe,
            "active": active,
            "cost": cost,
            "photo": photo
        }
    if request.method == 'POST':
        id = request.form.get('id')
        product = db.session.query(Products).filter(Products.id == id).first()
        product.name = request.form.get('name')
        product.describe  = request.form.get('describe')
        product.active  = 1
        product.cost = request.form.get('cost')
        product.photo = request.form.get('photo')
        db.session.add(product)
        flash('El producto fue modificado con exitó')
        db.session.commit()
        return redirect(url_for('admin.consult'))
    return render_template("update.html", product = dicProducto)

@admin.route("/delete", methods=["GET"])
@roles_required('admin')
def delete():
    id = request.args.get('id')
    print(id)
    product = db.session.query(Products).filter(Products.id == id).first()
    product.active = 0
    
    db.session.add(product)
    db.session.commit()
    
    flash('El producto fue eliminado con exitó')

    return redirect(url_for('admin.consult'))

 