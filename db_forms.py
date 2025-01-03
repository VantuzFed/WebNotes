from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4, max=20)])

class RegisterForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired(), Length(min=4, max=20)])
    e_mail = StringField('E-mail:', validators=[DataRequired(), Email(message="Введите корректный адресс электронной почты")])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4, max=20)])
    password_equal = PasswordField('Подтвердите пароль:', validators=[DataRequired(), Length(min=4, max=20),
            EqualTo('password', message="Пароли должны совпадать.")])

