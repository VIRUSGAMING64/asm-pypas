from .Tokens import *
from modules.utils import *
from .memory import *

class Expression:
    def __init__(self, expr):
        self.expr:str = expr
        self.type     = None

    def Token(self):
        self.expr = cleanStr(self.expr)
        res = Tokenize(self.expr)
        return Token(self.expr, LINE, res)
    
    def __dict__(self):
        return {
            "expr":self.expr,
            "type":self.type
        }
    

def TokenizeSource(code,output):
    
        lines = []
        p = 0
        for line in code:
            p +=1
            if line == "": continue #TODO esto se debe arreglar, lo deje asi por ahora
            ex = Expression(line)
            print("-" * 8)
            line = ex.Token()
            lines.append(line)
            for j in range(len(line.tokens)):
                if line.tokens[j].expr == "//":
                    line.tokens[j].type = COMMENT
                    line.tokens[j].tokens = line.tokens[j+1:]
                    del line.tokens[j+1:]
                    break

                if line.tokens[j].type == KEYWORD and j != 0:
                    output["Errors"].append(f"keyword not in the start of line [{p}]")
                    break

            for j in line.tokens:
                if j.type == INVALID:
                    output["Errors"].append(f"invalid token at line: {p}")
                print(j.type,j.expr)
        
        return lines
