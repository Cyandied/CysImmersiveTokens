import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from os import listdir, remove, mkdir
from os.path import isfile, join
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from backend.classes import *
from backend.main import *
import time


#Start server:
#flask --app server run --debug


UPLOAD_FOLDER = join("static","uploads")
ALLOWED_EXTENSIONS = {'png', 'webp'}

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="html")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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


    return render_template("home.html")

@app.route("/editor", methods=["GET", "POST"])
@login_required
def editor():
    userFolderExsits = session["user"]["id"] in listdir(app.config['UPLOAD_FOLDER'])
    userFolder = join(app.config['UPLOAD_FOLDER'], session["user"]["id"])
    uploadedImages = []
    if request.method == "POST":
        form = request.form
        files = request.files
        if "button" in form:
            if form["button"] == "upload-images":
                if files and "images" in files:
                    for file in files.getlist("images"):
                        if allowed_file(file.filename):
                            if not (userFolderExsits):
                                mkdir(userFolder)
                            file.save(join(userFolder, file.filename))
            elif form["button"] == "purge-images":
                images = listdir(userFolder)
                if images and userFolderExsits:
                    for file in images:
                        remove(join(userFolder, file))

    
    if userFolderExsits:
        uploadedImages = listdir(userFolder)

    return render_template("editor.html",userfolder = userFolder.replace("static",""), images = uploadedImages, layers = np.arange(1,len(uploadedImages)+1))

@app.route("/alpha", methods=["GET", "POST"])
@login_required
def alpha():
    alpha = listdir("static/alpha")
    return alpha

@app.route("/modifyAlpha", methods=["GET", "POST"])
@login_required
def modifyAlpha():
    response= request.get_json()
    hex = response["color"]
    image = response["alpha"]
    userFolder = join(app.config['UPLOAD_FOLDER'], session["user"]["id"])
    alpha = join(userFolder,image)
    newAlpha = changeColor([alpha],HEXtoRGB([hex]),1)[0]
    name, extention = image.split(".")
    name = f'{name}_{time.time()}.{extention}'
    newAlpha.save(join(userFolder, name),"PNG")
    return {"new-image":join(userFolder, name).replace("static","")}

@app.route("/fetchTest", methods=["GET", "POST"])
@login_required
def fetchTest():
    myDict = {
        "name":"test"
    }
    data = request.get_json()
    print(data)


    return data