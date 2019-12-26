from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, InventoryForm, AddIngredientForm
from app.models import User, Ingredient
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Thomas'}
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    form = InventoryForm()
    form.ingredient_name.choices = [(str(ing.id), ing.name + ' (' + ing.quantity_type + ')') \
                                    for ing in Ingredient.query.order_by('name')]
    if form.validate_on_submit():
        if form.change_type.data == '1':
            current_user.add_inventory(ingredient_id=form.ingredient_name.data, quantity=form.quantity.data)
        else:
            current_user.remove_inventory(ingredient_id=form.ingredient_name.data, quantity=form.quantity.data)
        flash('Your inventory has been changed!')
        return redirect(url_for('inventory'))

    page = request.args.get('page', 1, type=int)
    inventories = current_user.inventories.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('inventory', page=inventories.next_num) if inventories.has_next else None
    prev_url = url_for('inventory', page=inventories.prev_num) if inventories.has_prev else None

    return render_template('inventory.html', title='Inventory', form=form, inventories=inventories.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/ingredients', methods=['GET', 'POST'])
@login_required
def ingredients():
    form = AddIngredientForm()
    if form.validate_on_submit():
        ingredient = Ingredient(name=form.ingredient_name.data, quantity_type=form.quantity_type.data)
        if Ingredient.query.filter_by(name=ingredient.name).first():
            flash('Ingredient already exists.')
        else:
            db.session.add(ingredient)
            db.session.commit()
            flash('New ingredient added!')

    page = request.args.get('page', 1, type=int)
    ingredients = Ingredient.query.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('inventory', page=ingredients.next_num) if ingredients.has_next else None
    prev_url = url_for('inventory', page=ingredients.prev_num) if ingredients.has_prev else None

    return render_template('ingredients.html', title='Ingredients', form=form, ingredients=ingredients.items,
                           next_url=next_url, prev_url=prev_url)
