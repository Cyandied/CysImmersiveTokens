from PIL import Image as img
from os.path import join

def changeColor(paths:list, newColors:list):
    alphas = []
    wh = []
    for i, path in enumerate(paths):
        picture = img.open(path)
        width, height = picture.size
        wh.append([width,height])
        for x in range(width):
            for y in range(height):
                currentColor = picture.getpixel((x,y))
                color = (newColors[i][0],newColors[i][1],newColors[i][2],currentColor[-1])
                if currentColor != (0,0,0,0):
                    picture.putpixel((x,y), color)
        alphas.append(picture)
    return alphas,wh[0]

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

