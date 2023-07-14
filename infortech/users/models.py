from infortech import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False)
    address = db.Column(db.String(200), unique=False)
    NIF = db.Column(db.Integer, nullable=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(180), unique=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.name


class JsonEncodeDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class UserOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    order_NIF = db.Column(db.Integer, unique=False)
    order_total = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    orders = db.Column(JsonEncodeDict)

    def __repr__(self):
        return '<UserOrder %r>' % self.invoice
