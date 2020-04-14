# coding: utf-8

import os
import re
import shutil
import argparse

# Setting
debuglog = True
distFolderName = "html/"
srcFolderName = "html_src/"
basePath = "./"

reg_pattern = r'<!--\s*#include\s*virtual="(.*?)"\s*-->'
reg_fileName_pattern = r'.*\.(html|css|md)'
reg_copy_fileName_pattern = r'.*\.(png)'


# command line
parser = argparse.ArgumentParser(
    prog="resolveHtmlInclude",
    usage="transfer template html file to html",
    description="description",
    epilog="end",
    add_help=True
)

parser.add_argument("-c","--clear", help="clear transformed files", action='store_true')

args = parser.parse_args()

##

distPath = basePath + distFolderName
srcPath = basePath + srcFolderName


# print(list)


textCache = {}

def modifyFileName(fileName:str)->str:
    if fileName[0:1] == "/":
        return fileName[1:]

    return fileName

def getTemplateText(fileName:str)->str:

    templatePath:str = srcPath + modifyFileName(fileName)

    if templatePath in textCache:
        return textCache[templatePath]

    text = ""    

    text = transform(templatePath)

    debugLog("save cache:" + templatePath)
    textCache[templatePath] = text

    return text


def texttransformLine(line:str) -> str:    
    match = re.search(reg_pattern, line)
    if match:
        templateFile :str = match.group(1)
        templateText = getTemplateText(templateFile)
        replaceText = re.sub(reg_pattern, templateText, line)
        return replaceText

    return line

                






            


def transform(filePath:str) -> str:

    lines = []
    with open(filePath, encoding='utf-8') as f:
        lines = f.readlines()

    out_lines = []
    for line in lines:
        out_lines.append(texttransformLine(line))

    ret = "".join(out_lines)
    return ret



def write(path:str, text):
    debugLog("write:"+path)
    debugLog(" "+text[:10]+"...")

    with open(path, "w", encoding='utf-8') as f:
        f.write(text)

def copyFile(fromPath:str, toPath:str):
    debugLog("copy:"+fromPath)
    shutil.copyfile(fromPath, toPath)

def copyFolder(fromPath:str, toPath:str):
    debugLog("copyFolder:"+fromPath)
    # If it doesn't exist, copy it and be done.
    if not os.path.exists(toPath):
        shutil.copytree(fromPath, toPath)
        # os.makedirs(toPath)
        # debugLog(" makeDir:"+fromPath)
        return
    
    # Let's take a look inside.
    for item in os.listdir(fromPath):
        src = os.path.join(fromPath, item)
        dist = os.path.join(toPath, item)
        # If it's a file, we' ll copy it.
        if os.path.isfile(src):
            debugLog(" copy:"+item)
            shutil.copyfile(src, dist)
            continue
        # If it's a folder, it's processed recursively.
        if os.path.isdir(src):
            copyFolder(src, dist)
            continue
        
        debugLog("[Warning]exception type:"+item)





def removeFiles(path:str):
     fileNames = os.listdir(path)
     for fileName in fileNames:
        if checkFileName(fileName) or checkCopyFileName(fileName):
             filePath = path + fileName
             debugLog("remove:" + filePath)
             removeFile(filePath)




def removeFile(path:str):
    os.remove(path)




def debugLog(text:str):
    if debuglog:
        print(text)

def checkFileName(fileName:str)->bool:
    match = re.search(reg_fileName_pattern, fileName)
    if match:
        return True
    
    return False

def checkCopyFileName(fileName:str)->bool:
    match = re.search(reg_copy_fileName_pattern, fileName)
    if match:
        return True
    
    return False

def isFolder(fileName:str, basePath:str)->bool:
    path = os.path.join(basePath, fileName)
    return os.path.isdir(path)

## execution part


def mainMethod():
 os.makedirs(distPath, exist_ok=True)
 removeFiles(distPath)

 list = os.listdir(srcPath)
# filename display
 for filename in list:
    debugLog("check:"+filename)
    filePath = srcPath + filename

    # In the meantime, I'll copy the folder...
    if isFolder(filename, srcPath):
        debugLog(" -> folder")    
        toPath = distPath + filename
        copyFolder(filePath, toPath)
        continue

    if checkCopyFileName(filename):
        debugLog(" -> copy file")    
        toPath = distPath + filename
        copyFile(filePath, toPath)
        continue

    if checkFileName(filename) == False:
        debugLog("skip...")
        continue

    # file reading

    replacedText = transform(filePath)

    distFilePath = distPath + filename

    write(distFilePath, replacedText)


def main():
    if args.clear:
        debugLog("clear")
        removeFiles(distPath)
        return

    mainMethod()


main()



       







