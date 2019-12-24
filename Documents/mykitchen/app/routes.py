from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Thomas'}
    inventorys = [{
        'item': {'name': 'Chicken'},
        'quantity': 1,
        'quantity_type': 'pound'
    },
        {
            'item': {'name': 'Onion'},
            'quantity': 2,
            'quantity_type': 'cup'
        }
    ]
    return render_template('index.html', title='Home', user=user, inventorys=inventorys)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)