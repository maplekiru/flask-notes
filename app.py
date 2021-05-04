"""Flask app for Notes"""

from flask import Flask, jsonify, request, render_template, flash, session, redirect

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from project_secrets import API_SECRET_KEY
from forms import NewUserForm

app = Flask(__name__)

app.config['SECRET_KEY'] = API_SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

@app.route("/")
def route_to_register():
    """redirect to register route"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Show a form that when submitted will register/create a user"""

    form = NewUserForm()

    if form.validate_on_submit():
        # username = 
        # password = 
        # email = 
        # first_name = 
        # last_name = 
        return 5
    else:
        return render_template("user_register_form.html",
            form=form)