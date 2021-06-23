from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField
from wtforms.validators import DataRequired,Length,Email

class RichTextForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired(),Length(1,50)])
    body=TextAreaField('Body',validators=[DataRequired()])
    publish=SubmitField('Publish')
    save=SubmitField('Save')

class SignForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(1,20)])
    password=PasswordField('password',validators=[DataRequired(),Length(8,128)])
    signin=SubmitField('Sign in')

class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(1,20)])
    password=PasswordField('password',validators=[DataRequired(),Length(8,128)])
    email=StringField('Email',validators=[DataRequired(),Email(),Length(1,128)])
    register=SubmitField('Register')

