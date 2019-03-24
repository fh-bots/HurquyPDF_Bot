from os import path as pathx, listdir, remove, mkdir
from glob import glob
from secrets import token_urlsafe
from pdf2image import convert_from_path
import tempfile
from gestion_pdf import listPDF
from time import sleep
from shutil import rmtree

# Method for verficate if exists the path with document
def verificate(chatID):
    chat_ID = str(chatID)
    pathz = "./PDFs/" + chat_ID
    if(pathx.exists(pathz) and (len(glob(pathz + "/*" + ".pdf"))>0)):
        return True
    else:
        return False

# Method for create the directory
def createDir(chatID):
    chat_ID = str(chatID)
    pathzDIrectory = "./imagenes/" + chat_ID
    if(pathx.exists(pathzDIrectory)):
        return pathzDIrectory
    else:
        mkdir(pathzDIrectory)
        return pathzDIrectory


# Method for convert of PDF to images 
def createPDFtoImages(chatID):
    pathz = listPDF(chatID)
    with tempfile.TemporaryDirectory() as path:
        imagesFromPath = convert_from_path(pathz, output_file=path)
    saveDir = createDir(chatID)
    i = 1
    for page in imagesFromPath:
        if(1 <= 10):
            baseFileName = str(i) + ".jpg"
            page.save(pathx.join(saveDir, baseFileName), "JPEG")
            i+=1
        else:
            print("limit for extract is of 10 images")


# Method for list of the images with path
def listImages(chatID):
    count = 0
    # path where the folder is located the images of the user
    pathz = "./imagenes/" + str(chatID) + "/"
   
    # count of PDFs = 1
    listPdf = listdir(pathz)
    images = []

    # extract 10 images
    for listUNit in listPdf:
        if(listUNit.endswith(".jpg")):
            if(count <=10):
                a = pathz + listUNit
                images.append(a)
                count = count + 1
    images.sort()

    # return <= 10 images with paths
    return images


# Method for delete all the images
def deleteAllImages(chatID):
    pathz = "./imagenes/" + str(chatID) + "/"
    rmtree(pathz)