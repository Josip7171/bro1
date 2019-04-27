from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    search = StringField('', description="Unesi pojam")
    submit2 = SubmitField('Pretraži')
