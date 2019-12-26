from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Ingredient


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class InventoryForm(FlaskForm):
    ingredient_name = SelectField('Ingredient', validators=[DataRequired()])
    change_type = RadioField(validators=[DataRequired()], choices=[('1', 'Add'), ('-1', 'Remove')])
    quantity = FloatField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddIngredientForm(FlaskForm):
    ingredient_name = StringField('Ingredient Name', validators=[DataRequired()])
    quantity_type = StringField('Quantity Type', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Edit ingredient form

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')