from modules.generic.utils import *
from modules.interpreter.t_statics import *
import functools

@functools.lru_cache()
def Tokenize(code: str) -> list[Token]:

    pos = 0
    act_tok = ""
    tokens = []
    start_str = None
    in_str = False

    while pos <= len(code):

        if (pos < len(code)) and ((not code[pos] in operators) or in_str):
            act_tok += code[pos]

            if start_str == None and code[pos] in ["\"", "\'"]:
                in_str = not in_str
                start_str = code[pos]
            
            elif code[pos] == start_str:
                in_str = not in_str
                start_str = None

        else:
            dis = -1        
            act_tok = cleanStr(act_tok)
            tokens.append(Token(act_tok,NIL))

            if pos < len(code):            
                dis -= 1
            
            p = False
            if act_tok == "":
                tokens.pop()
                p = True

            if dis == -2:
                tokens.append(Token(code[pos], OPERATION))
                if pos + 1 != len(code) and code[pos] + code[pos + 1] in operators:
                    tokens[len(tokens) - 1].expr += code[pos + 1]
                    pos += 1
         
            if p: 
                pos += 1
                continue
        
            t_token = tokens[len(tokens) + dis]
            le = len(t_token.expr)
            if t_token.expr.isnumeric():
                t_token.type = NUMBER
                t_token.expr = int(t_token.expr)
            elif t_token.expr.startswith("\"") and t_token.expr.endswith("\"") and le > 1:
                t_token.type = STRING
                t_token.expr = t_token.expr.removeprefix("\"").removesuffix("\"")
            elif t_token.expr.startswith("'") and t_token.expr.endswith("'") and le > 1:
                t_token.type = STRING
                t_token.expr = t_token.expr.removeprefix("\'").removesuffix("\'")
            elif t_token.isKeyword():
                t_token.type = KEYWORD
            elif t_token.isLabel():
                t_token.type = LABEL
            elif t_token.VarName():
                t_token.type = VARIABLES
                t_token.data["name"] = t_token.expr
            
            act_tok = ""

        pos += 1


    line_tokens = []
    for i in range(len(tokens)):
        line:Token = tokens[i]
        if line.type == NIL:
            splited_tokens = line.getErrs()
            for t in splited_tokens:
                if t == []:
                    continue
                line_tokens.append(t[0])        
        else:
            line_tokens.append(line)
            
    return line_tokens

class Token:
    def __init__(self,expr, type = NIL, tokens = None):
        self.expr:str = expr
        self.type = type
        self.tokens  = tokens
        self.data = {}

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

    def __mod__(self, other):
        return self.expr % other.expr

    def __ne__(self, value):
        if isinstance(value , Token):
            return self.expr != value.expr
        return self.expr != value

    def __truediv__(self, other):
        return self.expr // other.expr

    def __add__(self, other):
        return self.expr + other.expr

    def __mul__(self, other):
        return self.expr * other.expr 

    def __sub__(self, other):
        return self.expr - other.expr

    def __hash__(self):
        return self.expr.__hash__()
    
    def __abs__(self):
        return self.expr.__abs__()
    
    def __and__(self, other):
        return self.expr and other.expr

    def __le__(self, other):
        return self.expr < other.expr

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
    
    def getErrs(self):
        self.expr = self.expr.split(' ')
        
        if len(self.expr) == 1:
            return [[Token(self.expr[0],INVALID)]]
    
        arr = []
        for x in self.expr:
            arr.append(Tokenize(x))

        return arr
    

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
    return 