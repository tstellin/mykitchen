from app import create_app, db
from app.models import Recipe, User, Ingredient
from flask_login import current_user
import unittest
from config import Config


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_METHODS = []
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


def register():
    u = User(username='test123', email='test123@aol.com', password_hash='cat')
    db.session.add(u)
    db.session.commit()

class MainRecipesModel(unittest.TestCase):


    def setUp(self):
        app = create_app(TestConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()
        db.create_all()
        register()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.app.post(
            'auth/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def add_recipe(self, submitted_by_user_id,
                   name='TestRecipe', instructions='Do Stuff',
                   servings=2, follow_redirects=True):
        onion = Ingredient(name='onion',
                           quantity_type='Cup',
                           calories_per_serving=50)
        chicken = Ingredient(name='Chicken',
                             quantity_type='Pound',
                             calories_per_serving=75)
        return self.app.post(
            'recipes',
            data=dict(submitted_by_user_id=submitted_by_user_id, name=name, instructions=instructions,
                      servings=servings),
            follow_redirects=follow_redirects
        )
    """
    def test_valid_recipe_added(self):
        with self.app:
            self.login('test123', 'cat')
            response = self.add_recipe(submitted_by_user_id=1, follow_redirects=False)
            self.assertEqual(200, response.status_code)
    """
