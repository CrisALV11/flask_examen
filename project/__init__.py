import os
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from decouple import config
db = SQLAlchemy()
from .models import User, Role, Products
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Método de inicio de la aplicación
def create_app():
    # Creación de instancia de la clase Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    db.init_app(app)

    @app.before_first_request
    def create_all():
        print('Hola')
        db.create_all()

    security = Security(app, user_datastore)

    # Registro del blueprint para las rutas auth de la aplicación
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint)

    # Registro del blueprint para las rutas no auth de la aplicación
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app




