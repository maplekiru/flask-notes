"""Flask app for Notes"""

from flask import Flask, jsonify, request, render_template, flash, session, redirect

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from project_secrets import FLASK_SECRET_KEY
from forms import NewUserForm, LoginForm, NewNoteForm

app = Flask(__name__)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY
# sqlalchemy echo to true - helps debug
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
    """Show a form that when submitted will register/create a user
        if user already logged in, redirects to user profile """

    if "user_id" in session:
        username = session["user_id"]
        return redirect(f"/users/{username}")
  

    form = NewUserForm()

    if form.validate_on_submit():
        user = {
            "username":form.username.data,
            "password":form.password.data,
            "email":form.email.data,
            "first_name":form.first_name.data,
            "last_name":form.last_name.data,
        }

        new_user = User.register(**user)
        
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.username

        
        return redirect(f'/users/{new_user.username}')
        
    else:
        return render_template("user_register_form.html",
            form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """ Checks if user is logged in and if not, 
        shows form that will log in user with authenticated credentials
        when submitted. Accepts username & password """

    if "user_id" in session:
        username = session["user_id"]
        return redirect(f"/users/{username}")

    
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
        in session - if so, renders user profile """

    if "user_id" not in session:
        flash("User access not allowed - must be logged in")
        return redirect('/')
    else:
        if session["user_id"] == username:
            user = User.query.get(username)

            return render_template('user_profile.html',
                user=user)
        
        return redirect("/login")


@app.route("/users/<username>/delete")
def delete_user(username):
    """ checks user authorization and deletes user
        from database if authorized """
    
    if "user_id" not in session:
        flash("User access not allowed - must be logged in")
        return redirect('/')
    
    if session["user_id"] != username:
        flash("Not allowed")
        return redirect('/')

    user = User.query.get(username)
    
    for note in user.notes:
        db.session.delete(note)

    db.session.delete(user)
    db.session.commit()

    session.pop("user_id", None)

    return redirect('/')


# NOTES ROUTES START -----------------------------------------------------------

@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_new_note(username):
    """ display form to add a new note and 
        adds new note to user notes """

    form = NewNoteForm()

    if "user_id" not in session:
        flash("User access not allowed - must be logged in")
        return redirect('/')
    else:
        if session["user_id"] == username:
            if form.validate_on_submit():

                title = form.title.data
                content = form.content.data
                note = Note(title=title, content=content, owner=username)

                db.session.add(note)
                db.session.commit()

                return redirect(f"/users/{username}") 
            else:
                return render_template("note_add_new.html", form=form)

        return redirect("/login")
        
@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def edit_note(note_id):
    """ Displays form to edit existing note and 
        makes changes to note """
    
    note =  Note.query.filter_by(id = note_id).first()
    
    if note is None:
        flash("This note does not exist")
        return redirect("/login")

    username = note.user.username
    form = NewNoteForm(obj = note)

    if "user_id" not in session:
        flash("User access not allowed - must be logged in")
        return redirect('/')
    else:
        if session["user_id"] == username:
            if form.validate_on_submit():
                note.title = form.title.data
                note.content = form.content.data

                db.session.commit()

                return redirect(f"/users/{username}")
            else:
                return render_template("note_edit_form.html", form=form)


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    """ Deletes note and redirects to user's profile """

    note =  Note.query.filter_by(id = note_id).first()

    if note is None:
        flash("This note does not exist")
        return redirect("/login")

    username = note.user.username

    if "user_id" not in session:
        flash("User access not allowed - must be logged in")
        return redirect('/')
    else:
        if session["user_id"] == username:
            db.session.delete(note)
            db.session.commit()
            return redirect(f"/users/{username}")


            


