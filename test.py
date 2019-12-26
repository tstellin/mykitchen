import unittest
from app import app, db
from app.models import User, Ingredient, Recipe, Inventory


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

        u = User(username='Test', email='Test@Example.com')
        ing = Ingredient(name='Rice', quantity_type='Cup')
        db.session.add_all([ing, u])
        self.u = User.query.first()
        self.ingredient_id = Ingredient.query.filter_by(name='Rice').first().id

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_ingredient_in_inventory(self):
        self.assertEqual(self.u.ingredient_in_inventory(ingredient_id=self.ingredient_id), None)

        user_id = User.query.first().id
        self.u.inventories.append(Inventory(ingredient_id=self.ingredient_id, user_id=user_id, quantity=1))

        self.assertEqual(self.u.ingredient_in_inventory(ingredient_id=self.ingredient_id).ingredient_id, self.ingredient_id)
        self.assertEqual(self.u.ingredient_in_inventory(ingredient_id=self.ingredient_id).quantity, 1)

    def test_add_inventory(self):
        self.u.add_inventory(ingredient_id=self.ingredient_id, quantity=1)

        self.assertEqual(self.u.inventories.count(), 1)

        quantity = self.u.inventories.filter_by(ingredient_id=self.ingredient_id).first().quantity
        self.assertEqual(quantity, 1)

        self.u.add_inventory(ingredient_id=self.ingredient_id, quantity=2)

        quantity = self.u.inventories.filter_by(ingredient_id=self.ingredient_id).first().quantity
        self.assertEqual(quantity, 3)

    def test_remove_inventory(self):
        user_id = User.query.first().id
        self.u.inventories.append(Inventory(ingredient_id=self.ingredient_id, user_id=user_id, quantity=1))

        self.u.remove_inventory(ingredient_id=self.ingredient_id, quantity=.5)
        quantity = self.u.inventories.filter_by(ingredient_id=self.ingredient_id).first().quantity
        self.assertEqual(quantity, .5)

        self.u.remove_inventory(ingredient_id=self.ingredient_id, quantity=5)
        quantity = self.u.inventories.filter_by(ingredient_id=self.ingredient_id).first().quantity
        self.assertEqual(quantity, 0)
