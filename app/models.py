from datetime import datetime
from app import db

recipe_ingredients = db.Table('ingredients',
                       db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                       db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')))



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    inventories = db.relationship('Inventory', backref='owner', lazy='dynamic')

    def add_inventory(self, ingredient_id, quantity):
        pass

    def ingredient_is_in_inventory(self, ingredient_id):
        return self.inventories.filter()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Inventory(db.Model):
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, primary_key=True)

    quantity = db.Column(db.Integer)

    def __repr__(self):
        return 'fix later'

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True)
    instructions = db.Column(db.Text)
    servings = db.Column(db.Integer)
    total_calories = db.Column(db.Integer)
    calories_per_serving = db.Column(db.Integer)

    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients,
        primaryjoin=(recipe_ingredients.c.recipe_id == id),
        secondaryjoin=(recipe_ingredients.c.ingredient_id == id),
                                  backref=db.backref('recipes', lazy='dynamic'), lazy='dynamic')


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    quantity_type = db.Column(db.String(140))