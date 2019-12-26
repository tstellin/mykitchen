from app import app, db
from app.models import User, Inventory, Recipe, Ingredient

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Inventory': Inventory, 'Recipe': Recipe, 'Ingredient': Ingredient}