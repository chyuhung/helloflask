from flask_wtf import FlaskForm
from wtforms import TextAreaField,validators,SubmitField
from wtforms.validators import DataRequired


class NewNoteForm(FlaskForm):
    body=TextAreaField('Body',validators=[DataRequired()])
    submit=SubmitField('Save')

# class EditNoteForm(FlaskForm):
#     body=TextAreaField('Body',validators=[DataRequired()])
#     submit=SubmitField('Update')

class EditNoteForm(NewNoteForm):
    submit=SubmitField('Update')

class DeleteNoteForm(FlaskForm):
    submit=SubmitField('Delete')