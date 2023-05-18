from PIL import Image as img
from os import listdir
from os.path import isfile, join
import numpy as np
import math

listIconType = []
listFiles = []

# def changeColor(image:str,newColor:tuple):
#     picture = img.open(f'alpha/{image}_alpha.png')
#     width, height = picture.size
#     color = (newColor[0], newColor[1], newColor[2], 255)
#     for x in range(width):
#         for y in range(height):
#             currentColor = picture.getpixel((x,y))
#             if currentColor != (0,0,0,0):
#                 picture.putpixel((x,y), color)
#     return picture

def scaleImage(image, scale:float):
    return image.resize((math.floor(1000*scale),math.floor(1000*scale)))

def changeColor(paths:list, newColors:list, scale:float):
    alphas = []
    for i, path in enumerate(paths):
        picture = scaleImage(img.open(path), scale)
        width, height = picture.size
        color = (newColors[i][0],newColors[i][1],newColors[i][2],255)
        for x in range(width):
            for y in range(height):
                currentColor = picture.getpixel((x,y))
                if currentColor != (0,0,0,0):
                    picture.putpixel((x,y), color)
        alphas.append(picture)
    return alphas

def addLayer(bottom, top):
    return img.alpha_composite(bottom,top)
    
def genarateIcon(images:list, name:str, bgtype:str, newColors:list, scale:float):
    alphas = changeColor(images, newColors, scale)
    background = scaleImage(img.open(f'backgrounds/{bgtype}_background.png'), scale)
    glowEffect = scaleImage(img.open(f'backgrounds/gloweffect/{name}_gloweffect.png'), scale)
    lines = scaleImage(img.open(f'foregrounds/{name}_lines.png'), scale)
    image = addLayer(background, glowEffect)
    for alpha in alphas:
        image = addLayer(image, alpha)
    image = addLayer(image,lines)
    return image
    
        


# def genarateIcon(image:str, backgroundType:str, newColor:tuple):
#     alpha = changeColor(image,newColor)
#     background = img.open(f'backgrounds/{backgroundType}Background.png')
#     glowEffect = img.open(f'backgrounds/glowEffect/{image}_gloweffect.png')
#     foreground = img.open(f'foregrounds/{image}_lines.png')
#     background = img.alpha_composite(background,glowEffect)
#     background = img.alpha_composite(background,alpha)
#     background = img.alpha_composite(background,foreground)
#     return background

def saveIconSmall(images:list, bgtype:str, name:str, newColors:list,dest:str, scale:float):
    icon = genarateIcon(images,name, bgtype, newColors,scale)
    icon.save(f'{dest}/temp_temp_icon.PNG', "PNG")

def saveIcon(images:list, bgtype:str, name:str, newColors:list,personalizedName:str,dest:str, scale = 1):
    icon = genarateIcon(images,name, bgtype, newColors, scale)
    icon.save(f'{dest}/{name}_{personalizedName}_icon.PNG', "PNG")

def HEXtoRGB(HEXs:list) -> tuple:
        RGBs = []
        for HEX in HEXs:
            _, HEX = HEX.split("#")
            RGB = tuple(int(HEX[i:i+2], 16) for i in (0, 2, 4))
            RGBs.append(RGB)
        return RGBs

def getFiles():
    global listIconType
    global listFiles
    onlyfilesIconType = [f for f in listdir("alpha") if isfile(join("alpha", f))]
    nameListIconType = []
    nameListUnique = []
    for entry in onlyfilesIconType:
        name,_ = entry.split("_")
        nameListIconType.append(name)
        if name not in nameListUnique:
            nameListUnique.append(name)
    listFiles = np.array(onlyfilesIconType)
    listIconType = np.array(nameListIconType)
    return nameListUnique

def findAlphas(name:str):
    mask = (name == listIconType)
    return listFiles[mask], np.arange(len(listFiles[mask]))
