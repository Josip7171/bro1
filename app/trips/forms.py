from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, InputRequired, NumberRange
from flask_wtf.file import FileAllowed, FileField


class CreateTripForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired(), Length(min=3, max=30)])
    user_id = StringField('Author')
    price = IntegerField('Price', validators=[InputRequired(), NumberRange(min=1, max=1000000)])
    people_number = IntegerField('Spaces Available', validators=[InputRequired(), NumberRange(min=2, max=100)])
    starting_at = DateTimeField('Starting Date', format="%d-%m-%Y %H:%M")
    transport_type = StringField('Transport', validators=[DataRequired()])
    trip_duration = IntegerField('Trip Duration', validators=[InputRequired(), NumberRange(min=1, max=31)])
    details = TextAreaField('Description',validators=[DataRequired(message='...')])
    trip_picture = FileField('Update trip picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Go')
