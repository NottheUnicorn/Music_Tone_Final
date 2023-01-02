from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class SongForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    guitar = StringField('Guitar', validators=[DataRequired()])
    amp = StringField('Amp', validators=[DataRequired()])
    pedals = StringField('Pedals', validators=[DataRequired()])
    style = StringField('Style', validators=[DataRequired()])
    groove = StringField('Groove', validators=[DataRequired()])
    submit = SubmitField('Edit')
