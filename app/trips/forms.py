from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, InputRequired, NumberRange
from flask_wtf.file import FileAllowed, FileField


class CreateTripForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)], description="Name")
    location = StringField('Location', validators=[DataRequired(), Length(min=3, max=30)], description="Location")
    user_id = StringField('Author', description="User ID")
    price = IntegerField('Price', validators=[InputRequired(), NumberRange(min=1, max=1000000)], description="Price")
    people_number = IntegerField('Spaces Available', validators=[InputRequired(), NumberRange(min=2, max=100)],
                                 description="Number of People")
    starting_at = DateTimeField('Starting Date', format="%d-%m-%Y %H:%M", description="Starting Date")
    transport_type = StringField('Transport', validators=[DataRequired()], description="Transport Type")
    trip_duration = IntegerField('Trip Duration', validators=[InputRequired(), NumberRange(min=1, max=31)],
                                 description="Trip Duration")
    details = TextAreaField('Description',validators=[DataRequired(message='...')], description="Details")
    trip_picture = FileField('Update trip picture', validators=[FileAllowed(['jpg', 'png'])], description="Trip Picture")
    submit = SubmitField('Go')
