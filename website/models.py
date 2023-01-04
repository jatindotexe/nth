

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    nutritional_info = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    image = db.Column(db.String(1000))
    barcode_image = db.Column(db.LargeBinary)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    usertype = db.Column(db.String(20))


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.String(10))
    message = db.Column(db.String(1000))



