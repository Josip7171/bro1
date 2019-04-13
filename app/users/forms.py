from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                     ValidationError, RadioField, DateField, TextAreaField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2,max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2,max=25)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2,max=51)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[Length(min=3, max=60)])
    country = StringField('Country', validators=[Length(min=3, max=30)])
    phone_number = StringField('Phone number', validators=[Length(min=8, max=25)])
    gender = RadioField('Spol', choices=[('male', 'musko'), ('female', 'zensko')])
    birth_date = DateField('Birth date', format='%d-%m-%Y')
    about_me = StringField('About me', validators=[Length(min=2, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This User already exists. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This Email is already taken. Please choose another one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[Length(min=3, max=60)])
    country = StringField('Country', validators=[Length(min=3, max=30)])
    phone_number = StringField('Phone number', validators=[Length(min=8, max=25)])
    about_me = TextAreaField('About me', validators=[Length(min=2, max=120)])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This User already exists. Please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This Email is already taken. Please choose another one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])
    submit = SubmitField('Reset Password')


