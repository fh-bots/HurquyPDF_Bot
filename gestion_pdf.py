from secrets import token_urlsafe
from os import path,mkdir,getcwd,remove, listdir
from time import sleep
from glob import glob
from shutil import rmtree 
from PyPDF2 import PdfFileReader


# Method for save the document
def savePDF(namePDF, download):
    try:
        with open(namePDF, "wb")as new_PDF:
            new_PDF.write(download)
            new_PDF.close()
        pdfFileObject = open(namePDF, "rb")
        pdfReader = PdfFileReader(pdfFileObject)
        deletePDF(namePDF)
        return True
    except: 
        print("error with the PDF")
        remove(namePDF)
        return False
    
    
    
# Method for create the directory wwith namePDF
def createDirectoryPDF(chatID):
    cadenaAleatoria = token_urlsafe(15)
    namePDF = str(chatID) + "_" + cadenaAleatoria + ".pdf"
    chat_id = str(chatID)
    nameDirectory = "./PDFs/" + chat_id

    if(path.exists(nameDirectory)):
        rutaPDF = nameDirectory + "/" + namePDF
        return rutaPDF
    else:
        mkdir(nameDirectory)
        rutaPDF = nameDirectory + "/" + namePDF
        return rutaPDF

# Method for delete PDF
def deletePDF(namePDF):
    sleep(300)
    if(path.exists(namePDF)):
        remove(namePDF)
    else:
        print("deleted")

def countPDFs(chatID):
    chat_id = str(chatID)
    pathz = "./PDFs/" + chat_id
    return len(glob(pathz + "/*" + ".pdf"))


def deleteAllPDF(chatID):
    chat_id = str(chatID)
    pathz = "./PDFs/" + chat_id
    rmtree(pathz)

# Method for list PDF on the directory with path <=1
def listPDF(chatID):
    count = 0
    pathz = "./PDFs/" + str(chatID) + "/"
    listPdf = listdir(pathz)

    for listUNit in listPdf:
        if(listUNit.endswith(".pdf")):
            if(count <=1):
                a = pathz + listUNit
                count = count + 1
    return a