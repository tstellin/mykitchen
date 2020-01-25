from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, FloatField, TextAreaField,\
    IntegerField, SelectMultipleField, FieldList
from wtforms.validators import DataRequired


class InventoryForm(FlaskForm):
    ingredient_name = SelectField('Ingredient', validators=[DataRequired()])
    change_type = RadioField(validators=[DataRequired()], choices=[('1', 'Add'), ('-1', 'Remove')])
    quantity = FloatField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddIngredientForm(FlaskForm):
    ingredient_name = StringField('Ingredient Name', validators=[DataRequired()])
    quantity_type = StringField('Quantity Type', validators=[DataRequired()])
    calories_per_serving = IntegerField('Calories per Servings', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RecipeIngredientForm(FlaskForm):
    submit = SubmitField('Submit')


class AddRecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired()])
    ingredients = SelectMultipleField('Ingredients', coerce=int)
    submit = SubmitField('Submit')
