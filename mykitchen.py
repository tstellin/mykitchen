from app import app, db
from app.models import User, Inventory, Recipe, Ingredient


def make_shell_context():
    return {'db': db, 'User': User, 'Inventory': Inventory, 'Recipe': Recipe, 'Ingredient': Ingredient}