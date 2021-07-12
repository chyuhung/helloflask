from flask_wtf import FlaskForm
from wtforms import SubmitField,TextField
from wtforms.validators import DataRequired,Email

class Sendmail(FlaskForm):
    subject=TextField('subject',validators=[DataRequired()])
    to=TextField('to',validators=[DataRequired(),Email()])
    body=TextField('body',validators=[DataRequired()])
    submit=SubmitField('Send')