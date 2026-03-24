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
            raise Exception(f"Invalid function declaration at line [{self.i}]")

        toks = self.decl.tokens
        novars = []
        if toks[1].type != VARIABLES or toks[2].expr != "(":
            raise Exception(f"invalid token in function declaration at line [{self.i}]")
        
        for pointer in range(3, len(toks), 2):
            try:
                try:
                    var = toks[pointer]
                    comma = toks[pointer + 1]
                except Exception as e:
                    if (var.expr == ")") and pointer == 3:
                        break
                    raise Exception(f"Invalid token in function declaration at line [{self.i}]")
                
                if var.type != VARIABLES:
                    raise Exception(f"Invalid function declaration at line [{self.i}]")
               
                novars.append(var.expr)      
                
                if comma.expr == ")":
                    if (pointer + 2 != len(toks)):
                        raise Exception(f"Invalid function declaration at line [{self.i}]")
                    break

                if comma.expr != ',':       
                    raise Exception(f"invalid token in function declaration [{self.i}]")
                
            except Exception as e:
                raise e

        self.novars = novars
        self.name = toks[1].expr
        print(novars,set(novars))
        if len(novars) != len(set(novars)):
            raise Exception(f"Invalid function declaration at line [{self.i}]")


    def Token(self):
        return Token(
            self.name,
            FUNC,
          self.code.tokens
        )
    



class Evaluator:
    def __init__(self,structure:Token = None, start = None, output = {},memory = None):
        self.pos = start if start is not None else 0
        self.out = output
        self.exceptions = []
        self.Tree = structure
        self.memory = memory
        if self.Tree is None:
            raise Exception("The source tree is None")


    def run(self):
        while self.step():
            print(f"Executed line: [{self.pos+1}]")
            if len(self.out['Errors']) >= 1:
                break

        print("---" * 3, "memory audit", "---" * 3)
        debug.audit_memory(self.memory)

    def step(self):
        self.execute(self.Tree.tokens[self.pos])
        self.pos += 1
        if self.pos >= len(self.Tree.tokens):
            return False

        return True

    def execute(self, line):
        if line.tokens == None:
            return

        if len(line.tokens) == 0:
            return

        if line.type == CONDITION:
            self.execute_condition(line)

        elif line.type == FUNC:
            self.execute_func(line)            
        elif line.tokens[0].expr == 'var':
            try:
                if line.tokens[1].type != VARIABLES or line.tokens[2].expr != "=":
                    raise "error"
            
                value,err = Expression(None, self.memory).evalTokens(line.tokens[3:])
                if len(value) != 1 or len(err) != 0:
                    raise Exception("Invalid declaration")

                value = value[0].expr
                self.memory.alloc_var(line.tokens[1].expr,value)
                
            except Exception as e:
                if isinstance(e,ZeroDivisionError):
                    self.out["Errors"].append(f"Zero division error at line [{line.get("line","unknow")}]")
                self.out["Errors"].append(f"Invalid variable declaration at line [{line.get('line','unknow')}]")
        else:
            print(line.expr)

    def execute_condition(self, line):
        print("condition: ",[x.expr for x in line.data["condition"]])
        
        value,err = Expression(None, self.memory).evalTokens(line.data["condition"])
        if len(value) != 1 or len(err) != 0:
            raise Exception("Invalid condition")

        line.data["condition"] = value[0].expr
        print(value[0].expr)

        if line.data["condition"]:
            for i in line.tokens:
                self.execute(i)

    def execute_func(self, line):
        pass

    def jump(self, pos):
        self.pos = pos
