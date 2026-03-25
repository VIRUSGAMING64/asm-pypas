from .Tokens import *
from .Expression import *
import modules.interpreter.debug as debug

class IF: 
    err = []
    def __init__(self,linenumer ,decl, code = None):
        self.code = None

        if len(decl.tokens) < 2:
            raise Exception(f"invalid declaration at line [{decl.get('line', 'unknow')}]")  
            
        self.cond = decl.tokens[1:]
        self.code = code
        self.expr = decl.expr

    def Token(self):
        tok =  Token(
                self.expr,
            CONDITION,
            self.code.tokens
        )
        tok.data["condition"] = self.cond
        return tok

class FUNCS: 
    def __init__(self,start, lines):
        self.code   = None
        self.decl   = lines[start]
        self.i      = self.decl.get("line", "unknow")
        self.novars = []
        self.declaration()

    def declaration(self):
        if len(self.decl.tokens) < 4:
            raise DeclarationException(FUNC, self.i)
        toks = self.decl.tokens
        novars = []
        if toks[1].type != VARIABLES or toks[2].expr != "(":
            raise DeclarationException(FUNC, self.i)
        for pointer in range(3, len(toks), 2):
            try:
                try:
                    var = toks[pointer]
                    comma = toks[pointer + 1]
                except Exception as e:
                    if (var.expr == ")") and pointer == 3:
                        break
                    raise DeclarationException(FUNC, self.i)
                
                if var.type != VARIABLES:
                    raise DeclarationException(FUNC, self.i)      
                
                novars.append(var.expr)      
                
                if comma.expr == ")":
                    if (pointer + 2 != len(toks)):
                        raise DeclarationException(FUNC, self.i)
                    break

                if comma.expr != ',':       
                    raise DeclarationException(FUNC, self.i)
                
            except Exception as e:
                raise e

        self.novars = novars
        self.name = toks[1].data["name"]
        print(novars,set(novars))
        if len(novars) != len(set(novars)):
            raise Exception(f"Invalid function declaration at line [{self.i}]")


    def Token(self):
        return Token(
            self.name,
            FUNC,
          self.code.tokens
        )
    
