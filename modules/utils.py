import mimetypes
import flask

def read(path, mode = "rb"):
    file = open(path,mode)
    data = file.read(2**30)
    file.close()
    return data

def getmimetype(path):
    return mimetypes.guess_type(path)[0]

def response(file):
    return flask.Response(read(file), mimetype=getmimetype(file))

def CleanCode(code):
    b = True
    ncode = ""
    for c in code:
        if c == " " and b:
            continue
        if c == "\"" or c == "\'":
            b = not b
        ncode += c
    return ncode

def PosOf(elem, lis:list):
    try:
        return lis.index(elem)
    except:
        return None

def cleanStr(s: str) -> str:
    while s.startswith(" "):
        s = s.removeprefix(" ")
    while s.endswith(" "):
        s = s.removesuffix(" ")
    return s

