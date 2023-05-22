import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from os import listdir, remove, mkdir
from os.path import isfile, join
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from backend.classes import *
from backend.main import *
import numpy as np
import time
import werkzeug


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

@app.route("/login", methods=["GET", "POST"])
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

@app.route("/", methods=["GET", "POST"])
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
                ogs = form.getlist("og-images")
                if userFolderExsits:
                    for file in listdir(userFolder):
                        if file not in ogs:
                            remove(join(userFolder, file))
                if files and "images" in files:
                    for file in files.getlist("images"):
                        if len(file.read()) > 3*1000*1000:
                            flash(f'Sorry, your file: {file.filename} is too big, the limit is 3 MB per file')
                        elif allowed_file(file.filename):
                            if not (userFolderExsits):
                                mkdir(userFolder)
                            print(file)
                            file.save(join(userFolder, file.filename))
            elif form["button"] == "purge-images":
                images = listdir(userFolder)
                if images and userFolderExsits:
                    for file in images:
                        remove(join(userFolder, file))
            elif form["button"] == "purge-top":
                images = listdir(userFolder)
                if images and userFolderExsits:
                    for file in images:
                        tag = file.split(".")[0].split("_")[-1]
                        if tag not in ["background","bg"]:
                            remove(join(userFolder, file))
            elif "delete-image" in form["button"]:
                image = form["button"].split("\\")[1]
                remove(join(userFolder,image))

    
    if userFolderExsits:
        uploadedImages = listdir(userFolder)
        # if uploadedImages:
        #     normalize(userFolder,uploadedImages)

    layers = np.arange(1,len(uploadedImages)+1)
    uploadedImages.sort()

    return render_template("editor.html",userfolder = userFolder.replace("static",""), images = uploadedImages, layers = layers[::-1])

@app.route("/tutorial", methods=["GET", "POST"])
def tutorial():
    path = join("static","images","exsample")
    exampleImages = listdir(path)
    zIndexes = [5,4,3,1,2,6]
    exzs = []
    names = []
    for i, image in enumerate(exampleImages):
        exzs.append([image, zIndexes[i]])
    
    for html in listdir(join("html","tutorialParts")):
        name = html.split(".")[0]
        if name != "tutorial":
            names.append(name)

    def get_zIndex(exz):
        return exz[1]
    
    exzs.sort(key = get_zIndex, reverse=True)

    return render_template("tutorialParts/tutorial.html" , path = path.replace("static",""), exz = exzs, names = set(names) )

@app.route("/modifyAlpha", methods=["GET", "POST"])
@login_required
def modifyAlpha():
    t1 = time.time()
    pixels = 0
    response= request.get_json()
    hex = response["color"]
    image = response["alpha"]
    name, extention = image.split(".")
    userFolder = join(app.config['UPLOAD_FOLDER'], session["user"]["id"])
    alpha = join(userFolder,image)

    for pic in listdir(userFolder):
        picName = pic.split(".")[0]
        if picName == "your_icon":
            remove(join(userFolder,pic))
        if name in picName and name != picName:
            remove(join(userFolder,pic))

    newAlpha,wh = changeColor([alpha],HEXtoRGB([hex]))
    name = f'{name}_{time.time()}.{extention}'
    newAlpha[0].save(join(userFolder, name),"PNG")
    t2 = time.time()
    tdelta = t2-t1
    ppert = (wh[0]*wh[1])/tdelta
    print(tdelta,ppert," in seconds")
    return {"new-image":join(userFolder, name).replace("static","")}

@app.route("/save", methods=["GET","POST"])
@login_required
def save():
    response= request.get_json()
    userFolder = join(app.config['UPLOAD_FOLDER'], session["user"]["id"])
    image = genarateIcon(userFolder, response)
    image.save(join(userFolder, "your_icon.png"),"PNG")

    return {"link":join(userFolder, "your_icon.png").replace("static","")}

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash(f'You are now logged out! Hope to see you soon, {session["user"]["name"]}')
    session["user"] = None
    return redirect(url_for("home"))