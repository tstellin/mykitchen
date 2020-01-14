from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import current_app, db
from app.main.forms import InventoryForm, AddIngredientForm, AddRecipeForm, AmountForm
from app.models import Ingredient, Recipe
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    user = {'username': 'Thomas'}
    return render_template('main/index.html', title='Home', user=user)

@bp.route('/inventory', methods=['GET', 'POST'])
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
        return redirect(url_for('main.inventory'))

    page = request.args.get('page', 1, type=int)
    inventories = current_user.inventories.paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.inventory', page=inventories.next_num) if inventories.has_next else None
    prev_url = url_for('main.inventory', page=inventories.prev_num) if inventories.has_prev else None

    return render_template('main/inventory.html', title='Inventory', form=form, inventories=inventories.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/ingredients', methods=['GET', 'POST'])
@login_required
def ingredients():
    form = AddIngredientForm()
    if form.validate_on_submit():
        ingredient = Ingredient(name=form.ingredient_name.data,
                                quantity_type=form.quantity_type.data,
                                calories_per_serving=form.calories_per_serving.data)
        if Ingredient.query.filter_by(name=ingredient.name).first():
            flash('Ingredient already exists.')
        else:
            db.session.add(ingredient)
            db.session.commit()
            flash('New ingredient added!')

    page = request.args.get('page', 1, type=int)
    ingredients = Ingredient.query.paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.inventory', page=ingredients.next_num) if ingredients.has_next else None
    prev_url = url_for('main.inventory', page=ingredients.prev_num) if ingredients.has_prev else None

    return render_template('main/ingredients.html', title='Ingredients', form=form, ingredients=ingredients.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/recipes', methods=['GET', 'POST'])
@login_required
def recipes():
    form = AddRecipeForm()
    ingredients = Ingredient.query.all()
    form.ingredients.choices = [(i.id, i.name) for i in ingredients]
    if form.validate_on_submit():
        r = Recipe(name=form.name.data,
                   instructions=form.instructions.data,
                   servings=form.servings.data)
        ings = Ingredient.query.filter(id in form.ingredients.data).all()
        for ing in ings:
            r.ingredients.append(ing)
        db.session.add(r)
        db.session.commit()
        recipe_id = Recipe.query.filter_by(name=form.name.data).first().id
        return redirect(url_for('main.ingredient_detail', recipe_id=recipe_id))
    return render_template('main/recipes.html', title='Recipes', form=form)


@bp.route('/ingredient_detail', methods=['GET', 'POST'])
@login_required
def ingredient_detail():
    form = AmountForm()
    recipe_id = request.args.get('recipe_id')
    r = Recipe.query.filter_by(id=recipe_id).first()

    return render_template('main/ingredient_detail.html', form=form)