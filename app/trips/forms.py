from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CreateTripForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired(), Length(min=3, max=30)])
    user_id = StringField('Author')
    date_created = StringField('Date Created')
    # transport = StringField('Transport', validators=[DataRequired()])
    # spaces = IntegerField('Spaces Available', validators=[InputRequired(), NumberRange(min=1, max=100)])
    # start_date = DateTimeField('Starting Date format="%Y-%m-%d %H:%M:%S"")')
    # price = IntegerField('Price', validators=[InputRequired(), NumberRange(min=1, max=1000000)])
    # trip_duration = IntegerField('Trip Duration', validators=[InputRequired(), NumberRange(min=1, max=31)])
    details = TextAreaField('Description',validators=[DataRequired(message='...')])
    submit = SubmitField('Go')


