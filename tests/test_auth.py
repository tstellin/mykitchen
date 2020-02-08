from app import create_app, db
from app.models import User
import unittest
from unittest import mock
from config import Config
from tests.helper_methods import login, register, logout

#https://www.patricksoftwareblog.com/unit-testing-a-flask-application/

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_METHODS = []
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class AuthBlueprint(unittest.TestCase):

    def setUp(self):
        app = create_app(TestConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_logout_redirect(self):
        response = logout(self.app)
        self.assertEqual('http://localhost/index', response.location)

    def test_main_page(self):
        with self.app as a:
            register(self.app, 'test123', 'test123@aol.com', 'cat', 'cat', True)
            login(a, 'test123', 'cat', True)
            response = self.app.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = register(self.app, 'testuser', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome', True)
        self.assertEqual(200, response.status_code)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

    def test_valid_user_registration_redirect(self):
        response = register(self.app, 'testuser', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome', False)
        self.assertEqual('http://localhost/auth/login', response.location)

    def test_invalid_user_registration_different_passwords(self):
        response = register(self.app, 'testuser', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsNotAwesome', True)
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_invalid_user_registration_duplicate_email(self):
        response = register(self.app, 'testuser', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome', True)
        self.assertEqual(response.status_code, 200)
        response = register(self.app, 'testuser1', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome', True)
        self.assertIn(b'Please use a different email address.', response.data)

    def test_invalid_user_registration_duplicate_username(self):
        response = register(self.app, 'testuser', 'pat@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome', True)
        self.assertEqual(response.status_code, 200)
        response = register(self.app, 'testuser', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome', True)
        self.assertIn(b'Please use a different username.', response.data)

    @mock.patch('flask_login.utils._get_user')
    def test_current_user_is_authenticated_redirect(self, current_user):
        user = mock.MagicMock()
        current_user.is_authenticated = True
        response = self.app.get('auth/register', follow_redirects=False)
        self.assertEqual('http://localhost/index', response.location)

    @mock.patch('flask_login.utils._get_user')
    def test_login_current_user_is_authenticated_redirect(self, current_user):
        user = mock.MagicMock()
        current_user.is_authenticated = True
        response = self.app.get('auth/login', follow_redirects=False)
        self.assertEqual('http://localhost/index', response.location)

    def test_valid_user_login_redirect(self):
        user = User(username='tester', email='test@aol.com')
        user.set_password('abc123')
        db.session.add(user)
        db.session.commit()
        response = login(self.app, 'tester', 'abc123', follow_redirects=False)
        self.assertEqual('http://localhost/index', response.location)

    def test_user_login(self):
        user = User(username='tester', email='test@aol.com')
        user.set_password('abc123')
        db.session.add(user)
        db.session.commit()
        response = login(self.app, 'tester', 'abc123', follow_redirects=True)
        self.assertEqual(200, response.status_code)
        response = login(self.app, 'invalid', 'abc123', follow_redirects=False)
        self.assertEqual('http://localhost/index', response.location)

    def test_user_invalid_credentials(self):
        response = login(self.app, 'invalihhhhd', 'abc123', follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)
        response = login(self.app, 'tester', 'abc1234', follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)



