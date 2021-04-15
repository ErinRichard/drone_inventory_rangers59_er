from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField

# DataRequired and Email are classes, so we will need to instantiated them
from wtforms.validators import DataRequired, Email

# email, password, submit_button
# Validators is set to a list because we could have more than one
class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()
