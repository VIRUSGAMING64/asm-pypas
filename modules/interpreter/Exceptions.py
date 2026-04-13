
import logging
from .statics_values import *

def SimpreExceptionParser(e, out, line):
    e.line = line
    out["Errors"].append(e.GetError())
    return INVALID, None

class InterpreterException(Exception):
    def __init__(self, line, *args):
        super().__init__(*args)
        self.line = line
        self.line = self.GetLine()

    def GetError(self):
        return f"UNKNOW EXCEPTION AT LINE [{self.line}]"    

    def GetLine(self):
        if self.line == None:
            return "UNKNOW"
        if isinstance(self.line , int):
            return self.line
        self.line = self.line.data.get("line", None)
        return self.line

class BuiltinException(InterpreterException):
    def __init__(self, base, line=None, *args):
        super().__init__(line, *args)
        self.base = base

    def GetError(self):
        return str(self.base) + f" at line [{self.GetLine()}]"
    
class InvalidTokenException(InterpreterException):
    def __init__(self, token , line, *args):
        super().__init__(line, *args)
        self.token = token
    
    def GetError(self):
        return f"INVALID TOKEN EXCEPTION AT LINE [{self.line}]"

class ArithmeticException(InterpreterException):
    def __init__(self, line, *args):
        super().__init__(line, *args)

    def GetError(self):
        if self.line != None:
            self.line=self.GetLine()
            return f"INVALID ARICMETIC OPERATION AT LINE [{self.line}]"
        else:
            return f"INVALID OPERATION [{self.args}]"

class DeclarationException(InterpreterException):
    def __init__(self, type, line, *args):
        super().__init__(line, *args)
        self.type = type

    def GetError(self):
        return f"INVALID DECLARATION AT LINE [{self.line}]"
    

class InterpreterMemoryError(InterpreterException):
    def __init__(self, *args):
        self.args = args
        super().__init__(None, *args)

    def GetError(self):
        return self.args[0]

class GotoException(InterpreterException):
    def __init__(self, line, *args):
        super().__init__(line, *args)

    def GetError(self):
        return f"LABEL NOT FOUND EXCEPTION [{self.line}]"
    
class CallFuncException(InterpreterException):
    def __init__(self, line, *args):
        super().__init__(line, *args)

    def GetError(self):
        return f"function call exception[{self.line}]"

class ExpresionException(InterpreterException):
    def __init__(self, line, *args):
        super().__init__(line, *args)
    
    def GetError(self):
        return f"[INVALID EXPRESSION AT LINE {self.GetLine()}]"   
    
class LoopException(InterpreterException):
    def __init__(self, line, *args):
        super().__init__(line, *args)
    
    def GetError(self):
        return f"[Error excecuting loop {self.GetLine()}]"