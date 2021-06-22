import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models.user import User   
bcrypt = Bcrypt(app) 


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/reg", methods=["POST"])
def register_user():
    print("validating")
    # validate users info 
    if not User.validate_reg(request.form):
        print("not valid")
        return redirect("/")
    #hash the password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password" : pw_hash
    }
    print(request.form)
    user_id = User.create_user(data)
    
    flash("You've been registered. Please log in.")
    return redirect("/")


@app.route("/user/login", methods=['POST'])
def login_user():
    print(request.form)
    print("loggin_in")
    # create data to get the user by email in database
    data = {
        "email": request.form["email"]}
    # if theyre not the database prompt them to register
    user_in_db = User.get_user_by_email(data)
    print(user_in_db)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    #if their password doesnt match prompt them to try again
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    # else put their id into session 
    session["user_id"] = user_in_db.id
    session["first_name"] = user_in_db.first_name
    print("id in session")
    return redirect("/user/homepage")

@app.route("/user/homepage")
def user_homepage():
    if not "user_id" in session:
        return redirect("/")
    data = {
        "user_id": session["user_id"]
    }

    user = User.get_recipes(data)
    return render_template("login.html", user= user)



@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")