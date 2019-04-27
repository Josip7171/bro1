from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class CommentTripForm(FlaskForm):
    content = TextAreaField('Sadržaj', description='Sadržaj')
    submit = SubmitField('Objavi')
