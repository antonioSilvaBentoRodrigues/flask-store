from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    create_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email = first_name = db.Column(db.String(100),nullable=False, unique=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(250), nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    client_id = db.Column(db.Integer, nullable=False)
    total = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    second_address = db.Column(db.String(200), nullable=True)
    country = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    zip_code = db.Column(db.String(200), nullable=False)
    card_number = db.Column(db.String(20), nullable=False)






