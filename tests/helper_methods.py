from app.models import Ingredient




def register(self, username, email, password, password2, follow_redirects):
    return self.app.post(
        'auth/register',
        data=dict(username=username, email=email, password=password, password2=password2),
        follow_redirects=follow_redirects
    )

def login(self, username, password, follow_redirects):
    return self.app.post(
        'auth/login',
        data=dict(username=username, password=password),
        follow_redirects=follow_redirects
    )

def logout(self):
    return self.app.get(
        'auth/logout',
        follow_redirects=False
    )