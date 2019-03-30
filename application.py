import os
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from model import app, db, User, Features, Clients
from functions import login_required, reorder_priorities 
from tempfile import mkdtemp
import datetime
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "precious_two"
app.config["SECURITY_PASSWORD_SALT"] = "precious"

error = None

@app.route("/")
def home_page():
    session.clear()
    """login page"""
    return render_template("login.html")


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        if request.form.get("username")=="":
            error = "username field cannot be empty"
            return render_template("login.html", error = error)
        if request.form.get("password")=="":
            error = "password field cannot be empty"
            return render_template("login.html", error = error)
        # Query database for username
        rows = User.query.filter_by(username=request.form["username"].lower()).first()
        # Ensure username exists and password is correct
        if rows == None or not check_password_hash(rows.password, request.form.get("password")):
            error = "invalid username/password"
            return render_template("login.html", error = error)
        # Remember which user has logged in
        session["user_id"] = rows.id
        clients = Clients.query.all()
        features = Features.query.all()
        # return render portfolio
        return render_template("home.html", row = rows, clients = clients, features=features)
    else:
        try:
            session["user_id"]
        except KeyError:
            return render_template("login.html")
        else:
            rows = User.query.filter_by(id=session["user_id"]).first()
            clients = Clients.query.all()
            features = Features.query.all()
            # return render portfolio
            return render_template("home.html", row = rows, clients = clients, features=features)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("/login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure firstname was submitted
        if not request.form.get("firstname"):
            error = "you must provide  firstname"
            return render_template("register.html", error = error)
        # Ensure surname was submitted
        if not request.form.get("surname"):
            error = "you must provide your surname"
            return render_template("register.html", error = error)
        # Ensure email was submitted
        if not request.form.get("email"):
            error = "you must provide email"
            return render_template("register.html", error = error)
        # ensure the username is not taken
        username_check = User.query.filter_by(username=request.form.get("username").lower()).first()
        if  username_check:
            error = "username: "+request.form.get("username")+" already taken, choose another one"
            return render_template("register.html", error = error)
        email_check = User.query.filter_by(username=request.form.get("email")).first()
        if  email_check:
            error = "Another account has been opened with email: "+request.form.get("email")
            return render_template("register.html", error = error)
        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            error = "you must provide confirmation"
            return render_template("register.html", error = error)

        # Ensure password and confirmation match
        if (request.form.get("password") != request.form.get("confirmation")):
            error = "staff password and confirmation do not match"
            return render_template("register.html", error = error)
            
        user = User(firstname = request.form.get("firstname"), surname = request.form.get("surname"),email = request.form.get("email"), username = request.form.get("username").lower(), password = generate_password_hash(request.form.get("password")))
        db.session.add(user)
        db.session.commit()
        flash("user added")
        return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/username_check", methods=["POST"])
def register_check():
    if request.method == "POST":
        # Query database for username
        rows = User.query.filter_by(username=request.form.get("username").lower()).first()
        if not rows:
            return "true"
        else:
            return "false"


@app.route("/email_check", methods=["POST"])
def email_check():
    if request.method == "POST":
        # Query database for email
        rows = User.query.filter_by(email=request.form.get("email").lower()).first()
        if not rows:
            return "true"
        else:
            return "false"
            
@app.route("/login_check", methods=["POST"])
def login_check():
    if request.method == "POST":
        # Query database for username
        rows = User.query.filter_by(username=request.form.get('username').lower()).first()
        # Remember which user has logged in
        # Ensure username exists and password is correct
        if  rows == None or not check_password_hash(rows.password, request.form.get("password")):
            return "fail"
        else:
            return "true"

@app.route("/client_check", methods=["post"])
def client_check():
        # Query database for client
        rows = Clients.query.filter_by(name=request.form.get('name')).first()
        if  rows == None :
            return "true"
        else:
            return "fail"

        
@app.route("/add_client", methods=["POST", "GET"])
@login_required
def add_client():
    rows = User.query.filter_by(id=session["user_id"]).first()
    if request.method == "POST":
        if request.form.get("client_name") == "":
            error = "enter client name"
            return render_template("client_form.html",error=error, row = rows)
                # Query database for client
        rows = Clients.query.filter_by(name=request.form.get('client_name')).first()
        if (rows != None):
            error = "name already taken"
            return render_template("client_form.html",error=error, row = rows)

        client = Clients(name = request.form.get("client_name"))
        db.session.add(client)
        db.session.commit()
        client = Clients.query.all()
        feature = Features.query.all()
        flash("client added")
        # return render home page
        return render_template("home.html", row = rows, clients = client, features=feature)
    else:
        return render_template("client_form.html", row = rows)

@app.route("/add_feature", methods=["POST", "GET"])
@login_required
def add_feature():
    rows = User.query.filter_by(id=session["user_id"]).first()
    if request.method == "POST":
        if request.form.get("title") == "":
            error = "feature must have a title"
            client = Clients.query.all()
            return render_template("feature_form.html",error=error, row = rows, clients = client)
        if request.form.get("description") == "":
            error = "Describe feature"
            client = Clients.query.all()
            return render_template("feature_form.html",error=error, row = rows, clients = client)
        if request.form.get("priority") == "":
            error = "You must provide priority"
            client = Clients.query.all()
            return render_template("feature_form.html",error=error, row = rows, clients = client)
        if request.form.get("date") == "":
            error = "select target date"
            client = Clients.query.all()
            return render_template("feature_form.html",error=error, row = rows, clients = client)
        if request.form.get("client_id") == "":
            error = "select client name"
            client = Clients.query.all()
            return render_template("feature_form.html",error=error, row = rows, clients = client)
        if request.form.get("product_area") == "":
            error = "please select area"
            client = Clients.query.all()
            return render_template("feature_form.html",error=error, row = rows, clients = client)
        new_feature = Features(title = request.form.get("title"), description = request.form.get("description"),date_expected = request.form.get("date"), product_area = request.form.get("product_area"), priority = request.form.get("priority"), client_id=request.form.get("client_id"))
        db.session.add(new_feature)
        db.session.commit()
        client = Clients.query.all()
        feature = Features.query.all()
        reorder_priorities(int(request.form.get("client_id")))
        # return render home page
        return render_template("home.html", row = rows, clients = client, features=feature)
    else:
        client = Clients.query.all()
        return render_template("feature_form.html", row=rows, clients=client)