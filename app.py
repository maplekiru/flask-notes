"""Flask app for Notes"""

from flask import Flask, jsonify, request, render_template, flash, session, redirect

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from project_secrets import API_SECRET_KEY
from forms import NewUserForm, LoginForm

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
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.username

        
        return redirect(f'/users/{username}')
        
    else:
        return render_template("user_register_form.html",
            form=form)

@app.route("/login", methods=["GET", "POST"])
def login_user():
    """ Shows form that will log in user with authenticated credentials
        when submitted. Accepts username & password """
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username, password)
        if user:
            session["user_id"] = user.username
            return redirect(f'/users/{username}')
        else:
            flash("Incorrect username and/or password")
    
    return render_template("user_login_form.html", form=form)
        

@app.route("/logout")
def logout_user():
    """ clears user from session and returns to root route """

    session.pop("user_id", None)
    flash("Successfully logged out.")
    return redirect('/')

#USER ROUTES ---------------------------------------------------------

@app.route("/users/<username>")
def user_profile(username):
    """ checks if user is logged in by checking user_id
        in session - allows user to see "/secret" route
        if logged in """

    if "user_id" not in session:
        flash("User access not allowed - must be logged in")
        return redirect('/')
    else:
        user = User.query.get(username)

        return render_template('user_profile.html',
            user=user)


@app.route("/users/<username>/delete")
def delete_user(username):
    
    if "user_id" not in session:
        flash("User access not allowed - must be logged in")
        return redirect('/')
    else:
        user = User.query.get(username)
        
        for note in user.notes:
            db.session.delete(note)

        db.session.delete(user)
        db.session.commit()

        session.pop("user_id", None)

        return redirect('/')
