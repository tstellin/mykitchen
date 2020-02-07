from app.models import Ingredient

def register(client, username, email, password, password2, follow_redirects):
    return client.post(
        'auth/register',
        data=dict(username=username, email=email, password=password, password2=password2),
        follow_redirects=follow_redirects
    )


def login(client, username, password, follow_redirects):
    return client.post(
        'auth/login',
        data=dict(username=username, password=password),
        follow_redirects=follow_redirects
    )


def logout(client):
    return client.get(
        'auth/logout',
        follow_redirects=False
    )


def add_recipe(client, submitted_by_user_id,
                   name='TestRecipe', instructions='Do Stuff',
                   servings=2, follow_redirects=True):
        onion = Ingredient(name='onion',
                           quantity_type='Cup',
                           calories_per_serving=50)
        chicken = Ingredient(name='Chicken',
                             quantity_type='Pound',
                             calories_per_serving=75)
        return client.post(
            'recipes',
            data=dict(submitted_by_user_id=submitted_by_user_id, name=name, instructions=instructions,
                      servings=servings),
            follow_redirects=follow_redirects
        )