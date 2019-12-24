from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    inventories = db.relationship('Inventory', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    quantity = db.Column(db.Integer)
    quantity_type = db.Column(db.String(140))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Item: {}, Quantity: {} {}>'.format(self.name, self.quantity, self.quantity_type)