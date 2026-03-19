import mimetypes
import flask
from .t_statics import *


def getPrio(expr):
    if expr in P0:
        return 0
    if expr in P1:
        return 1
    if expr in P2:
        return 2
    else:
        return 4

def add(a,b):
    return a + b
def sub(a,b):
    return a - b
def div(a,b):
    return a / b
def mul(a,b):
    return a * b
def _not(a):
    return not a
def _or(a,b):
    return a or b
def _xor(a,b):
    return a ^ b
def _and(a,b):
    return a and b

operations = {
    "+":add,
    "-":sub,
    "*":mul,
    "/":div,
    "!":_not,
    "|":_or,
    "^":_xor,
    "&":_and
}

def _process_op(a,b,op):
    return operations[op](a,b)

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
        return -1

def cleanStr(s: str) -> str:
    while s.startswith(" "):
        s = s.removeprefix(" ")
    while s.endswith(" "):
        s = s.removesuffix(" ")
    return s

