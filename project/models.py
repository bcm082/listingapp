from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Products database

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String, nullable=False, unique=True)
    asin = db.Column(db.String, nullable=False, unique=True)
    upc = db.Column(db.Integer, nullable=True)
    parent_sku = db.Column(db.String, nullable=True)
    product_name = db.Column(db.String, nullable=False)
    product_description = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    bullet_point_1 = db.Column(db.String, nullable=True)
    bullet_point_2 = db.Column(db.String, nullable=True)
    bullet_point_3 = db.Column(db.String, nullable=True)
    bullet_point_4 = db.Column(db.String, nullable=True)
    bullet_point_5 = db.Column(db.String, nullable=True)
    image_1 = db.Column(db.String, nullable=True)
    image_2 = db.Column(db.String, nullable=True)
    image_3 = db.Column(db.String, nullable=True)
    image_4 = db.Column(db.String, nullable=True)
    image_5 = db.Column(db.String, nullable=True)
    image_6 = db.Column(db.String, nullable=True)
    image_7 = db.Column(db.String, nullable=True)
    video = db.Column(db.String, nullable=True)
    aplus_1 = db.Column(db.String, nullable=True)
    aplus_2 = db.Column(db.String, nullable=True)
    aplus_3 = db.Column(db.String, nullable=True)
    aplus_4 = db.Column(db.String, nullable=True)
    aplus_5 = db.Column(db.String, nullable=True)
    aplus_6 = db.Column(db.String, nullable=True)
    aplus_7 = db.Column(db.String, nullable=True)
    brand_name = db.Column(db.String, nullable=True)
