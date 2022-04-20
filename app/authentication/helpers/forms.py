from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, EqualTo, Email

class LoginForm(FlaskForm):
    email = StringField(label = 'Email', validators = [DataRequired(), Email()])
    password = PasswordField(label = 'Password', validators = [DataRequired()])
    submit = SubmitField(label = 'Login')

class RegisterForm(FlaskForm):
    email = StringField(label = 'Email', validators = [DataRequired(), Email()])
    password = PasswordField(label = 'Password', validators = [DataRequired()])
    password2 = PasswordField(label = 'Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField(label = 'Register')