from PIL import Image as img
from os.path import join
from os import remove

def deleteAllModifs(userFolder,file):
    fileTags = file.split("_")
    if "TEMPORARYFILEDELETETHIS" in fileTags:
        remove(join(userFolder, file))

def sizeAcceptable(file,mb:int):
    # accept = len(file.read()) > mb*1000*1000
    # return accept
    return True

def getTargetHeightWidth(path:str,filenames:list):
    hwsnorm = []
    hwsbg = []
    hws = None
    for filename in filenames:
        if filename.split(".")[0].split("_")[-1] in ["background", "bg"]:
            file = img.open(join(path,filename))
            hwsbg.append(file.size)
        else:
            file = img.open(join(path,filename))
            hwsnorm.append(file.size)

    def gettot(hw):
        return hw[1] + hw[0]
    if len(hwsbg) == 0:
        hwsnorm.sort(key=gettot)
        hws = hwsnorm
    else:
        hwsbg.sort(key=gettot)
        hws = hwsbg
    return hws[0]

def normalize(path:str,filenames:list,userSetSize:list = None):
    if not userSetSize:
        h,w = getTargetHeightWidth(path,filenames)
    else:
        h,w = userSetSize

    for filename in filenames:
        file = img.open(join(path,filename))
        fileh, filew = file.size
        if fileh != h or filew != w:
            file = file.resize((w,h))
            file.save(join(path, filename))


def changeColor(paths:list, newColors:list):
    alphas = []
    for i, path in enumerate(paths):
        picture = img.open(path)
        width, height = picture.size
        for x in range(width):
            for y in range(height):
                currentColor = picture.getpixel((x,y))
                color = (newColors[i][0],newColors[i][1],newColors[i][2],currentColor[-1])
                if currentColor != (0,0,0,0):
                    picture.putpixel((x,y), color)
        alphas.append(picture)
    return alphas

def addLayer(bottom, top):
    return img.alpha_composite(bottom,top)
    
def get_zIndex(image:dict):
    return image.get("z-index")

def getImage(fileName:str, mainpath:str):
    return img.open(join(mainpath, fileName))

def genarateIcon(mainpath:str, images:dict):
    images.sort(key=get_zIndex)
    fileNames = []
    for image in images:
        fileNames.append(image["name"])
    w,h = getImage(fileNames[0],mainpath).size
    image = img.new("RGBA",(w,h))
    for fileName in fileNames:
        image = addLayer(image, getImage(fileName,mainpath))
    return image

def HEXtoRGB(HEXs:list) -> tuple:
        RGBs = []
        for HEX in HEXs:
            _, HEX = HEX.split("#")
            RGB = tuple(int(HEX[i:i+2], 16) for i in (0, 2, 4))
            RGBs.append(RGB)
        return RGBs

