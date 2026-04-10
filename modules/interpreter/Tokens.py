from modules.generic.utils import *
from modules.interpreter.t_statics import *
import functools

class Token:
    def __init__(self,expr, type = NIL, tokens = [], data = {}):
        self.expr:str = expr
        self.type = type
        self.tokens  = tokens
        self.data = data
        self.data["name"] = self.expr

    def __dict__(self):
        di = {}
        di["expr"] = self.expr
        di["data"] = self.data
        di["type"] = self.type
        tok = self.tokens
        if isinstance(self.tokens, list):
            tok = []
            for target in self.tokens:
                target = target.__dict__()
                tok.append(target)
        di["tokens"] = tok
        return di

    def get(self,key,default):
        return self.data.get(key,default)
    
    def put(self, key ,data):
        self.data[key] = data

    def isKeyword(self):
        return self.expr in keywords
    
    def isOperator(self):
        return self.expr in operators
    
    def VarName(self):
        alphas = ""
        for i in self.expr:
            if i.isalnum():
                alphas+=i
            elif i != "_":
                return False
            
        if len(alphas) >= 1:
            return True
        
        print(alphas)
        return False
    
    def isLabel(self):
        return True if self.expr.endswith(":") else False
    
    def math(self, token):
        if token.expr in maths[self.expr]:
            return True
        return False
    

def dict2Token(di:dict):
    typ = di.get("type", None)
    expr = di.get("expr", None)
    tokens = di.get("tokens")
    data = di.get("data", None)

    if None in [typ, expr] or (tokens != None and not isinstance(tokens, list)):
        raise Exception("Invalid dict")
    
    if isinstance(tokens, list):
        toks = []
        for tok in tokens:
            tok = dict2Token(tok)
            toks.append(tok)
        tokens = toks
    n_tok = Token(expr , typ, tokens)
    n_tok.data = data
    return n_tok