import mimetypes
import flask
from ..interpreter.t_statics import *
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

def add(a,b):
    return a.expr + b.expr
def sub(a,b):
    return a.expr - b.expr
def div(a,b):
    return a.expr // b.expr
def mul(a,b):
    return a.expr * b.expr
def _not(a):
    return not a.expr
def _or(a,b):
    return a.expr or b.expr
def _xor(a,b):
    return a.expr ^ b.expr
def _and(a,b):
    return a.expr and b.expr

def eq(a, b):
    return a.expr == b.expr

def neg(a):
    return  -a.expr

def plus(a):
    return a.expr

def ge(a, b):
    return a.expr > b.expr

def le(a, b):
    return a.expr < b.expr

def leq(a, b):
    return a.expr <= b.expr

def geq(a, b):
    return a.expr >= b.expr

def mod(a, b):
    return a.expr % b.expr

def neq(a,b):
    return a.expr != b.expr

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
    "+":add,
    "-":sub,
    "*":mul,
    "/":div,
    "!":_not,
    "|":_or,
    "^":_xor,
    "&":_and,
    "!=": neq,
    "==": eq,
    "<=": leq,
    ">=": geq,
    "<": le,
    ">": ge,
    "=": asign,
    "%": mod
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