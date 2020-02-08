from unittest import TestCase
from app import create_app, db
from tests.helper_methods import register, login
from config import Config


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_METHODS = []
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class Test_Routes(TestCase):

    def setUp(self):
        app = create_app(TestConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()
        db.create_all()
        register(self.app, 'test123', 'test123@aol.com', 'cat', 'cat', True)

    def test_index(self):
        with self.app as a:
            login(a, 'test123', 'cat', True)
            response = self.app.get('index')
            self.assertEqual(200, response.status_code)
            self.assertIn(b'Hello, test123!', response.data)