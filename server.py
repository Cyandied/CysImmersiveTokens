import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from os import listdir, remove, mkdir
from os.path import isfile, join
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from backend.classes import *
from backend.main import *
import numpy as np
import time
import shutil
import requests as req


#Start server:
#flask --app server run --debug


UPLOAD_FOLDER = join("static","uploads")
ALLOWED_EXTENSIONS = {'png', 'webp'}
PBURL = "http://127.0.0.1:8090/api/collections"

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
    users = req.get(f'{PBURL}/users/records?expand=user_packs(user_id).pack_id').json()["items"]
    for user in users:
        packs = []

        for entry in user["expand"]["user_packs(user_id)"]:
            packs.append(entry["expand"]["pack_id"]["name"])

        if user_id == user["id"]:
            return User(user["username"], user["email"], user["role"], user["id"], packs)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        response = req.post(f'{PBURL}/users/auth-with-password?expand=user_packs(user_id).pack_id',json = {
            "identity" : request.form["user"],
            "password" : request.form["pass"]
        }).json()["record"]

        verified_user = False
        if "code" not in response:
            packs = []

            for entry in response["expand"]["user_packs(user_id)"]:
                packs.append(entry["expand"]["pack_id"]["name"])

            user = response
            verified_user = User(user["username"], user["email"], user["role"], user["id"],packs)
        
        if verified_user:
            session["user"] = verified_user.__dict__
            session["hw"] = None
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
    userpacks = {}
    basicTokens = {
        "items":["flask","crystalTypeChunk","stoneSmooth","statueTypeHumanoid","oreIngot","herbBranch"]
    }
    borders = listdir(join("static","bgs","borders"))
    backgrounds = listdir(join("static","bgs","bg"))

    for userpack in session["user"]["packs"]:
        packStorage = join("static","packs")
        packs = listdir(packStorage)
        if userpack in packs:
            userpacks[userpack] = listdir(join(packStorage,userpack))
        elif userpack == "all":
            for pack in packs:
                userpacks[pack] = listdir(join(packStorage,pack))
    if not session["user"]["packs"]:
        userpacks = basicTokens

    if request.method == "POST":
        form = request.form
        files = request.files
        if form["h"] and form["w"]:
            session["hw"] = [int(form["h"]),int(form["w"])]

        if userFolderExsits: #if the user has a folder
            for file in listdir(userFolder): #Check all files in user folder
                deleteAllModifs(userFolder,file)

        if "button" in form: #has a button been pressed?

            if form["button"] == "upload-images": #User uploads images

                if files and "images" in files: #Check if user has acutally uploaded images
                    for file in files.getlist("images"): #get uploaded images
                        if not sizeAcceptable(file, 3): #check size and disqualify if size too big
                            flash(f'Sorry, one or more of your files are too big, the limit is 3 MB per file, the offending files have not been imported to the editor.')
                        elif allowed_file(file.filename): #Check if filetype is acceptable
                            if not (userFolderExsits): #make a userfolder if it doesnt exsist already
                                mkdir(userFolder)
                            file.save(join(userFolder, file.filename)) #save file in userfolder

            elif form["button"] == "purge-images": #user deletes all images in thier folder
                images = listdir(userFolder)
                if images and userFolderExsits: #iterate over all images in the suer folder and delete
                    for file in images:
                        remove(join(userFolder, file))

            elif form["button"] == "purge-top": #user deletes all images with the exception of those with _bg or _background at the end
                images = listdir(userFolder)
                if images and userFolderExsits:
                    for file in images:
                        tags = file.split(".")[0].split("_") #Find _background or _bg tag
                        if not any(tag in ["background","bg"] for tag in tags):
                            remove(join(userFolder, file)) #Delete if not have the bg or background tag

            elif "delete-image" in form["button"]: #user deletes specefic image
                image = form["button"].split("\\")[1] #Find target image, used backspace to seprate value from image name since they are not allowed in filenames
                if image in listdir(userFolder):
                    remove(join(userFolder,image))
            
            elif form["button"] == "load":
                if userFolderExsits: #if the user has a folder
                    for file in listdir(userFolder): #Check all files in user folder
                        remove(join(userFolder,file))
                else:
                    mkdir(userFolder)

                if "tokens" in form and form["tokens"]:
                    pack, token = form["tokens"].split(",")
                    fromFolder = join("static","packs",pack,token)
                    for filename in listdir(fromFolder):
                        source = join(fromFolder,filename)
                        destination = join(userFolder,filename)
                        shutil.copy(source,destination)
                if "backgrounds" in form and form["backgrounds"]:
                    source = join("static","bgs","bg",form["backgrounds"])
                    destination = join(userFolder,form["backgrounds"])
                    shutil.copy(source,destination)
                if "borders" in form and form["borders"]:
                    source = join("static","bgs","borders",form["borders"])
                    destination = join(userFolder,form["borders"])
                    shutil.copy(source,destination)
    
    if userFolderExsits: #Update the images sent to Jinja
        uploadedImages = listdir(userFolder)
        if uploadedImages:
            if session["hw"] and type(session["hw"]) == list:
                if session["hw"][0] != 0 and session["hw"][1] != 0:
                    normalize(userFolder,uploadedImages,session["hw"])
            normalize(userFolder,uploadedImages)

    layers = np.arange(1,len(uploadedImages)+1)
    uploadedImages.sort()

    return render_template("editor.html",userfolder = userFolder.replace("static",""), images = uploadedImages, layers = layers[::-1], userpacks = userpacks, bgs = backgrounds, borders = borders, hw = session["hw"])

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

    newAlpha = changeColor([alpha],HEXtoRGB([hex]))
    name = f'{name}_\u221E_{time.time()}.{extention}'
    newAlpha[0].save(join(userFolder, name),"PNG")
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
    session["hw"] = None
    return redirect(url_for("home"))