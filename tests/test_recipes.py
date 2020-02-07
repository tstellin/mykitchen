from app import create_app, db
from tests.helper_methods import login, register, add_recipe
import unittest
from config import Config

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_METHODS = []
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class MainRecipesModel(unittest.TestCase):

    def setUp(self):
        app = create_app(TestConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()
        db.create_all()
        register(self.app, 'test123', 'test123@aol.com', 'cat', 'cat', True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_valid_recipe_added(self):
        with self.app:
           login(self.app, 'test123', 'cat', True)
           response = add_recipe(self.app, submitted_by_user_id=1, follow_redirects=True)
           self.assertEqual(200, response.status_code)

