from wtforms import StringField, PasswordField, TextAreaField
# can use EmailField and install 
from flask_wtf import FlaskForm

from wtforms.validators import InputRequired, Length

from models import User

class NewUserForm(FlaskForm):
    """Form for adding new user"""

    username = StringField("username", 
        validators=[InputRequired(),
            Length(max=20)])

    password = PasswordField("password", 
        validators=[InputRequired()])

    email = StringField("email", 
        validators=[InputRequired(),
            Length(max=50)])

    first_name = StringField("First Name", 
        validators=[InputRequired(),
            Length(max=30)])

    last_name = StringField("Last Name", 
        validators=[InputRequired(),
            Length(max=30)])


class LoginForm(FlaskForm):
    """ Form for logging in user """

    username = StringField("username", 
        validators=[InputRequired(),
            Length(max=20)])

    password = PasswordField("password", 
        validators=[InputRequired()])


class NewNoteForm(FlaskForm):
    """ Form for creating new Note """

    title = StringField("Note Title", 
        validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Note Content", 
        validators=[InputRequired()])  