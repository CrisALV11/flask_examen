import os
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .models import User, Role, Products
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Método de inicio de la aplicación
def create_app():
    # Creación de instancia de la clase Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jessi:1a2b3c@127.0.0.1:3306/flask_examen'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    db.init_app(app)

    @app.before_first_request
    def create_all():
        db.create_all()

    security = Security(app, user_datastore)

    # Registro del blueprint para las rutas auth de la aplicación
    from .admin import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Registro del blueprint para las rutas no auth de la aplicación
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app




