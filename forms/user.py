from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ChoiceForm(FlaskForm):
    melodrama = BooleanField('Мелодрама')
    family = BooleanField('Семейный')
    drama = BooleanField('Драма')
    comedy = BooleanField('Комедия')
    horror = BooleanField('Ужасы')
    joy = BooleanField('Радость')
    sadness = BooleanField('Грусть')
    loneliness = BooleanField('Одиночество')
    calmness = BooleanField('Спокойствие')
    inspiration = BooleanField('Вдохновлённое')
    adrenaline = BooleanField('Адреналин')
    submit = SubmitField('Подтвердить')
