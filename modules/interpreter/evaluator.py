from .Tokens import Token
import modules.interpreter.debug as debug
from .t_statics import *
from .Expression import Expression
from modules.interpreter.Exceptions import *

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
        audit = debug.audit_memory(self.memory)
        print(audit)
        self.out["result"] = audit

    def step(self):
        try:
            retcode = self.execute(self.Tree.tokens[self.pos],self.memory)
            if retcode == INVALID:
                return False
            self.pos += 1
            if self.pos >= len(self.Tree.tokens):
                return False
        except InterpreterMemoryError as e:
            self.out["Errors"].append(e.GetError())
            return False
        return True

    def execute(self, line, mem):
        if line.tokens == None:
            return EMPTY

        if len(line.tokens) == 0:
            return EMPTY

        if line.type == CONDITION:
            self.execute_condition(line, mem.copy())

        elif line.type == FUNC:
            self.execute_func(line, mem.copy())            
        elif line.tokens[0].expr == 'var':
            try:
                try:
                    if line.tokens[1].type != VARIABLES or line.tokens[2].expr != "=":
                        raise DeclarationException(VARIABLES, line, [])
                
                    value,err = Expression(None, mem).evalTokens(line.tokens[3:])
                
                    if len(value) != 1 or len(err) != 0:
                        raise DeclarationException(VARIABLES, line, [])
                    
                except DeclarationException as e:
                    if isinstance(e, DeclarationException):
                        self.out["Errors"].append(e.GetError())
                    return INVALID
                
                try:
                    value = value[0].expr
                    print(line.tokens[1].expr)
                    mem.alloc_var(line.tokens[1].data["name"],value)
                except InterpreterMemoryError as e:
                    self.out["Errors"].append(e.GetError())
                    return INVALID

            except InterpreterException as e:
                if isinstance(e, ArithmeticException):
                    e.line = line
                    self.out["Errors"].append(e.GetError())
                    return INVALID

                self.out["Errors"].append(f"python exception at line [{line.data["line"]}]:[{str(e)}]")
        else:
            Expression(None, self.memory).evalTokens(line)


    def execute_condition(self, line, mem):       
        value,err = Expression(None, mem).evalTokens(line.data["condition"])
        if len(value) != 1 or len(err) != 0:
            raise Exception("Invalid condition")

        line.data["condition"] = value[0].expr
        print(value[0].expr)

        if line.data["condition"]:
            for i in line.tokens:
                self.execute(i, mem)

    def execute_func(self, line):
        pass

    def jump(self, pos):
        self.pos = pos
