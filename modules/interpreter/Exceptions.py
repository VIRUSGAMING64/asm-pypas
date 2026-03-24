class InterpreterException(BaseException):
    def __init__(self, line, *args):
        super().__init__(*args)
        self.line = line
    def GetError(self):
        return f"UNKNOW EXCEPTION AT LINE [{self.line}]"    

class InvalidTokenException(InterpreterException):
    def __init__(self, token , line, *args):
        super().__init__(line, *args)
        self.token = token
    
    def GetError(self):
        return f"INVALID TOKEN EXCEPTION AT LINE [{self.line}]"

class AricmeticException(InterpreterException):
    def __init__(self, line, *args):
        super().__init__(line, *args)

    def GetError(self):
        return f"INVALID ARICMETIC OPERATION AT LINE [{self.line}]"

class DeclarationException(InterpreterException):
    def __init__(self, type, line, *args):
        super().__init__(line, *args)
        self.type = type
    
    def GetError(self):
        return f"INVALID DECLARATION AT LINE [{self.line}]"