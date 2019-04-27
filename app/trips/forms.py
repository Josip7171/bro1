from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired, NumberRange
from flask_wtf.file import FileAllowed, FileField


class CreateTripForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)], description="Name")
    location = StringField('Location', validators=[DataRequired(), Length(min=3, max=30)], description="Location")
    user_id = StringField('Author', description="User ID")
    price = IntegerField('Price', validators=[InputRequired(), NumberRange(min=1, max=1000000)], description="Price")
    people_number = IntegerField('Spaces Available', validators=[InputRequired(), NumberRange(min=2, max=100)],
                                 description="Number of People")
    starting_at = DateTimeField('Starting Date', format="%d-%m-%Y %H:%M", description="Starting Date (DD-MM-GGGG ss:mm)")
    transport_type = StringField('Transport', validators=[DataRequired()], description="Transport Type")
    trip_duration = IntegerField('Trip Duration', validators=[InputRequired(), NumberRange(min=1, max=31)],
                                 description="Trip Duration")
    is_private = BooleanField('Private?', id="checkboxOne")
    trip_password = StringField('Trip Password', description="Trip Password", id="tripPass")
    details = TextAreaField('Description',validators=[DataRequired(message='...')], description="Details")
    trip_picture = FileField('Update trip picture', validators=[FileAllowed(['jpg', 'png'])], description="Trip Picture")
    submit = SubmitField('Go')


class CommentTripForm(FlaskForm):
    content = TextAreaField('Sadržaj', description='Sadržaj')
    submit = SubmitField('Objavi')


class PasswordCheckForm(FlaskForm):
    trip_password = StringField('Trip Password', validators=[InputRequired()],
                                description="Trip Password", id="tripPass")
    submit = SubmitField('Prijavi se')
