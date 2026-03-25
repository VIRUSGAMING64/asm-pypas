
from modules.interpreter.Tokens import Token
import logging

class InterpreterException(BaseException):
    def __init__(self, line, *args):
        super().__init__(*args)
        self.line = line
        self.line = self.GetLine()

    def GetError(self):
        return f"UNKNOW EXCEPTION AT LINE [{self.line}]"    

    def GetLine(self):
        if isinstance(self.line , Token):
            self.line = self.line.data["line"]
        return self.line
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