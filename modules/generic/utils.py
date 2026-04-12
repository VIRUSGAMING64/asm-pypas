import mimetypes
import flask
from ..interpreter.statics_values import *
import functools
import logging

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

def _not(a):
    return not a.expr

def neg(a):
    return  -a.expr

def plus(a):
    return a.expr


una = {
    "-": neg,
    "+": plus,
    "!": _not
}

def asign(a, b, mem):
    a.expr = b.expr
    mem.Put(a.data["name"], a.expr)

def UnaryOP(a,op):
    return una[op.expr](a)

operations = {
    "+":lambda a, b: a.expr + b.expr,
    "-":lambda a, b: a.expr - b.expr,
    "*":lambda a, b: a.expr * b.expr,
    "/":lambda a, b: a.expr // b.expr,
    "!":lambda a:  not a.expr,
    "|":lambda a, b: a.expr | b.expr,
    "^":lambda a, b: a.expr ^ b.expr,
    "&":lambda a, b: a.expr & b.expr,
    "!=": lambda a, b: a.expr != b.expr,
    "==": lambda a, b: a.expr == b.expr,
    "<=": lambda a, b: a.expr <= b.expr,
    ">=": lambda a, b: a.expr >= b.expr,
    "<": lambda a, b: a.expr < b.expr,
    ">": lambda a, b: a.expr > b.expr,
    "=": asign,
    "%": lambda a, b: a.expr % b.expr
}

def process_op(b,a,op, mem):
    if op.expr == "=":
        return operations[op.expr](a,b,mem)
    return operations[op.expr](a,b)

def read(path, mode = "rb"):
    try:
        file = open(path,mode)
        data = file.read()
        file.close()
        return data
    except Exception as e:
        logging.log(logging.DEBUG,f"{e}")
        return b""

def getmimetype(path):
    return mimetypes.guess_type(path)[0]

def response(file, code = 200):
    return flask.Response(read(file), mimetype=getmimetype(file), status=code)

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


def GetType(p):
    if isinstance(p, int):
        return NUMBER
    elif isinstance(p, str):
        return STRING
    assert p != None
    return p.type