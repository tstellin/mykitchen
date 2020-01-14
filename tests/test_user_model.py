from flask import Flask
from app import create_app, db
from app.models import User, Ingredient, Inventory, Recipe
import unittest
from config import Config


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_METHODS = []
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app


    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        u = User(username='Test', email='Test@Example.com')
        ing1 = Ingredient(name='Rice', quantity_type='Cup', calories_per_serving=100)
        ing2 = Ingredient(name='Onion', quantity_type='Whole', calories_per_serving=75)
        db.session.add_all([ing1, ing2, u])
        self.u = User.query.first()
        self.ingredient_id1 = Ingredient.query.filter_by(name='Rice').first().id
        self.ingredients = Ingredient.query.all()

        self.u.add_recipe(
            'Test Recipe', 'Do this then that', 3, self.ingredients)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_ingredient_in_inventory(self):
        self.assertEqual(self.u.ingredient_in_inventory(ingredient_id=self.ingredient_id1), None)

        user_id = User.query.first().id
        self.u.inventories.append(Inventory(ingredient_id=self.ingredient_id1, user_id=user_id, quantity=1))

        self.assertEqual(self.u.ingredient_in_inventory(ingredient_id=self.ingredient_id1).ingredient_id, self.ingredient_id1)
        self.assertEqual(self.u.ingredient_in_inventory(ingredient_id=self.ingredient_id1).quantity, 1)

    def test_add_inventory(self):
        self.u.add_inventory(ingredient_id=self.ingredient_id1, quantity=1)

        self.assertEqual(self.u.inventories.count(), 1)

        quantity = self.u.inventories.filter_by(ingredient_id=self.ingredient_id1).first().quantity
        self.assertEqual(quantity, 1)

        self.u.add_inventory(ingredient_id=self.ingredient_id1, quantity=2)

        quantity = self.u.inventories.filter_by(ingredient_id=self.ingredient_id1).first().quantity
        self.assertEqual(quantity, 3)

    def test_remove_inventory(self):
        user_id = User.query.first().id
        self.u.inventories.append(Inventory(ingredient_id=self.ingredient_id1, user_id=user_id, quantity=1))

        self.u.remove_inventory(ingredient_id=self.ingredient_id1, quantity=.5)
        quantity = self.u.inventories.filter_by(ingredient_id=self.ingredient_id1).first().quantity
        self.assertEqual(quantity, .5)

        self.u.remove_inventory(ingredient_id=self.ingredient_id1, quantity=5)
        quantity = self.u.inventories.filter_by(ingredient_id=self.ingredient_id1).first().quantity
        self.assertEqual(quantity, 0)

    def test_add_recipe(self):
        r = self.u.recipes.first()
        self.assertEqual(r.total_calories, 175)
        self.assertEqual(r.calories_per_serving, 175/3)
        self.assertEqual(r.ingredients.count(), 2)
        ingredient_names = [ingredient.name for ingredient in r.ingredients.all()]
        self.assertEqual(set(ingredient_names), set(['Onion', 'Rice']))

    def test_delete_recipe(self):
        id = self.u.recipes.first().id
        self.u.delete_recipe(id)
        self.assertEqual(self.u.recipes.count(), 0)
        self.assertIsNone(self.u.recipes.filter_by(id=id).first())

    def test_use_recipe(self):
        self.u.use_recipe(1)