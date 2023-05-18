import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from os import listdir, remove
from os.path import isfile, join
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from backend.classes import *


#Start server:
#flask --app server run --debug

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="html")

app.secret_key = "i/2r:='d8$V{[:gHm5x?#YBB-D-6)N"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    print("getting json file")
    with open("users.json","r") as f:
        users = json.loads(f.read())
    print("Checking if user in users")
    for user in users:
        print("now checking user:", user["name"])
        print(f'Wanted id {user_id}, found id {user["id"]}')
        if user_id == user["id"]:
            print("user found in users")
            return User(user["name"], user["password"], user["role"], user["id"])

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        with open("users.json", "r") as f:
            users = json.loads(f.read())
            verified_user = False
        for user in users:
            if request.form["user"] == user["name"]:
                if request.form["pass"] == user["password"]:
                    verified_user = User(user["name"], user["password"], user["role"], user["id"])
                    break
        
        if verified_user:
            session["user"] = verified_user.__dict__
            login_user(verified_user)
            flash(f'sucessfully logged in! Welcome {session["user"]["name"]}')
            return redirect(url_for("home"))
        
        else:
            flash("Sorry, check if the username and password is correct.")
    
    
    return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        if "button" in request.form:
            return redirect(url_for(request.form["button"]))

    return render_template("home.html")

@app.route("/editor", methods=["GET", "POST"])
@login_required
def editor():

    return render_template("editor.html")