from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_msearch import Search
from flask_migrate import Migrate

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///infortech.db'
app.config['SECRET_KEY'] = 'acd39b027e648166cd1cf159c29131d2'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Login é necessário!"

from infortech.admin import routes
from infortech.products import routes
from infortech.users import routes
from infortech.suppliers import routes

from infortech.admin.models import Admin
from infortech.products.models import Product, Supplier, Category
from infortech.users.models import User, UserOrder
from infortech.suppliers.models import SupplierAccount

from infortech.cart import cart
