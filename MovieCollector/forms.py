from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo

'''
Registrazione
Username
email
password
confirm_password

Login:
email
password
remember_me
'''

class Registration(FlaskForm):

    username = StringField("Username", validators=[Length(min=2,max=10), DataRequired()])
    email = StringField("Email", validators=[Length(2,100), Email(), DataRequired()])
    #email = EmailField("Email", validators=[Length(2,100), DataRequired()])
    password = PasswordField("Password", validators=[Length(8,100), DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[Length(min=8,max=100,message = True), DataRequired(), EqualTo('password')])
    submit = SubmitField("Register Now!")

class Login(FlaskForm):

    email = EmailField("Email", validators=[Length(2,100), DataRequired()])
    password = PasswordField("Password", validators=[Length(min=8,max=100), DataRequired()])
    remember_me = BooleanField("Remember me: ")
    submit = SubmitField("Log in")
    