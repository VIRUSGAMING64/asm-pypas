from .Tokens import Token
import modules.interpreter.debug as debug
from .t_statics import *
from .Expression import Expression
from modules.interpreter.Exceptions import *
import time

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
  
        elif line.tokens[0].expr == 'var':
            try:
                return self.variable_declaration(line,mem)
            except DeclarationException as e:
                self.out["Errors"].append(e.GetError())
        elif line.tokens[0].type == LABEL:
            return EMPTY
        elif line.tokens[0].expr == "goto":
            try:
                return self.find_label(line, line.tokens[1].expr)
            except GotoException as e:
                self.out["Errors"].append(e.GetError())
        else:
            return self.run_line(line, mem)
        
    def run_line(self, line , mem):
        try:
            try:
                Expression(None, self.memory).evalTokens(line)
            except:
                Expression(None, mem).evalTokens(line)
        except InterpreterException as e:
            if isinstance(e, ArithmeticException):
                self.out["Errors"].append(e.GetError())
            return INVALID


    def find_label(self,line , name):
        name += ":"
        pos = -1
        for i in range(len(self.Tree.tokens)):
            pos += 1
            if self.Tree.tokens[i].expr == name:
                return self.jump(pos)
        raise GotoException(line)
    
    def execute_condition(self, line, mem):       
        value,err = Expression(None, mem).evalTokens(line.data["condition"])
        if len(value) != 1 or len(err) != 0:
            print(err, value)
            for t in value:
                print(t.expr, t.data.get("name", None))
            raise Exception("Invalid condition")
        x=value[0].expr
        print(x)

        if isinstance(x, Token):
            print(x.expr)
            time.sleep(10)

        if not value[0].expr:
            return self.jump(line.data["eoif"])
        for i in line.tokens:
            self.execute(i, mem)


    def execute_func(self, line, mem):
        pass #! TODO

    def jump(self, pos):
        self.pos = pos


    def variable_declaration(self, line, mem):
        try:
            try:
                if len(line.tokens) < 3 or line.tokens[1].type != VARIABLES or line.tokens[2].expr != "=":
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