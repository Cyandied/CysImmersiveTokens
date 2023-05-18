import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from os import listdir, remove
from os.path import isfile, join
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from backend.classes import *
from backend.main import *
import time


#Start server:
#flask --app server run --debug

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="html")

app.secret_key = "i/2r:='d8$V{[:gHm5x?#YBB-D-6)N"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with open("users.json","r") as f:
        users = json.loads(f.read())
    for user in users:
        if user_id == user["id"]:
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
    images = listdir("static/no-change")
    img_pos = []
    for image in images:
        _, pos = image.split("_")
        pos, _ = pos.split(".")
        img_pos.append([image,pos])

    return render_template("editor.html", imgpos = img_pos)

@app.route("/alpha", methods=["GET", "POST"])
@login_required
def alpha():
    alpha = listdir("static/alpha")
    return alpha

@app.route("/modifyAlpha", methods=["GET", "POST"])
@login_required
def modifyAlpha():
    hex = request.get_json()["color"]
    alpha = listdir("static/alpha")
    for pic in alpha:
        if pic != "flask_alpha.png":
            remove(f'static/alpha/{pic}')
    newAlpha = changeColor([f'static/alpha/{alpha[0]}'],HEXtoRGB([hex]),1)[0]
    name = f'{alpha[0].split(".")[0]}_{time.time()}.png'
    newAlpha.save(f'static/alpha/{name}',"PNG")
    return {"new-image":f'/alpha/{name}'}

@app.route("/fetchTest", methods=["GET", "POST"])
@login_required
def fetchTest():
    myDict = {
        "name":"test"
    }
    data = request.get_json()
    print(data)


    return data