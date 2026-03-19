import mimetypes
import flask
from .t_statics import *


def getPrio(expr):
    if expr.data.get("neg", False):
        return 3
    op = expr.expr
    if op in P0:
        return 0
    if op in P1:
        return 1
    if op in P2:
        return 2
    return -1

def isdelim(s):
    return True if s == " " else False

def is_operator(s):
    return True if s in operations else False

def is_unary(s):
    return True if s in ["+", "-", "!"] else False

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
def eq(a, b):
    return a == b
def neg(a):
    return  -a
def plus(a):
    return a
def ge(a, b):
    return a > b
def le(a, b):
    return a < b
def leq(a, b):
    return a <= b
def geq(a, b):
    return a >= b

una = {
    "-": neg,
    "+": plus,
    "!": _not
}

def UnaryOP(a,op):
    return una[op.expr](a)

operations = {
    "+":add,
    "-":sub,
    "*":mul,
    "/":div,
    "!":_not,
    "|":_or,
    "^":_xor,
    "&":_and,
    "==": eq,
    "<=": leq,
    ">=": geq,
    "<": le,
    ">": ge
}

def process_op(b,a,op):
    return operations[op.expr](int(a.expr),int(b.expr))

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

