from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField,\
    BooleanField, IntegerField, ValidationError, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, NumberRange
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
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


class CreateTripForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired(), Length(min=3, max=30)])
    user_id = StringField('Author')
    date_created = StringField('Date Created')
    # transport = StringField('Transport', validators=[DataRequired()])
    # spaces = IntegerField('Spaces Available', validators=[InputRequired(), NumberRange(min=1, max=100)])
    # start_date = DateTimeField('Starting Date format="%Y-%m-%d %H:%M:%S"")')
    # price = IntegerField('Price', validators=[InputRequired(), NumberRange(min=1, max=1000000)])
    # trip_duration = IntegerField('Trip Duration', validators=[InputRequired(), NumberRange(min=1, max=31)])
    details = TextAreaField('Description', validators=[DataRequired(message='Place small (or large) description here...')])
    submit = SubmitField('Go')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
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

