from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin
from time import time
import jwt

recipe_ingredients = db.Table('ingredients',
                              db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                              db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    inventories = db.relationship('Inventory', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ingredient_in_inventory(self, ingredient_id):
        return Inventory.query.filter_by(ingredient_id=ingredient_id,
                                         user_id=self.id).first()

    def add_inventory(self, ingredient_id, quantity):
        ingredient = self.ingredient_in_inventory(ingredient_id)
        if ingredient:
            ingredient.quantity = ingredient.quantity + quantity
        else:
            i = Inventory(ingredient_id=ingredient_id, user_id=self.id, quantity=quantity)
            db.session.add(i)

        db.session.commit()

    def remove_inventory(self, ingredient_id, quantity):
        ingredient = self.ingredient_in_inventory(ingredient_id)
        if ingredient:
            ingredient.quantity -= quantity
            if ingredient.quantity < 0:
                ingredient.quantity = 0
        db.session.commit()

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Inventory(db.Model):
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, primary_key=True)
    quantity = db.Column(db.Float)

    ingredient = db.relationship('Ingredient', backref='inventories')

    def __repr__(self):
        return '<ingredient_id {}>, user_id {}, quantity {}'.format(self.ingredient_id, self.user_id, self.quantity)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submitted_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    name = db.Column(db.String(140), index=True, unique=True)
    instructions = db.Column(db.Text)
    servings = db.Column(db.Integer)
    total_calories = db.Column(db.Integer)
    calories_per_serving = db.Column(db.Integer)

    __table_args__ = (db.UniqueConstraint(submitted_by_user_id, name), )

    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients,
                                  primaryjoin=(recipe_ingredients.c.recipe_id == id),
                                  secondaryjoin=(recipe_ingredients.c.ingredient_id == id),
                                  backref=db.backref('recipes', lazy='dynamic'), lazy='dynamic')


class Ingredient(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    submitted_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    name = db.Column(db.String(140), index=True)
    quantity_type = db.Column(db.String(140))
    calories_per_serving = db.Column(db.Integer)
    # Calories, other nut facts, etc

    inventory = db.relationship("Inventory")

@login.user_loader
def load_user(id):
    return User.query.get(int(id))