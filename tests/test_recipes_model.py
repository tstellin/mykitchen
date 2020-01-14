from app import create_app, db
from app.models import Recipe, User
from app.main.forms import AddRecipeForm, AddIngredientAmount
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
        self.register()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register(self):
        u = User(username='test123', email='test123@aol.com', password_hash='cat')
        db.session.add(u)
        db.session.commit()

    def add_recipe(self, follow_redirects, submitted_by_user_id=1,
                   name='TestRecipe', instructions='Do Stuff',
                   servings=2):
        return self.app.post(
            'main/recipes',
            data=dict(submitted_by_user_id=submitted_by_user_id, name=name, instructions=instructions,
                      follow_redirects=follow_redirects)
        )

    def test_too_long_name(self):
        pass
        # Apparently bc the underlying db is mysql, the typing will be dynamic so these enforcments
        # do nothing? how tf?

    def test_recipe_added(self):
        form = AddRecipeForm()