from .Tokens import *

class AST:
    def __init__(self):
        pass

    def eval(self,line:list[Token]):
        if len(line) < 1:
            raise Exception("line is empty")
        
        if len(line) == 1:
            return line[0]

        """
            !TODO
            variables assignation
            variables declaration
            function calls
            
        """


    def eval_func(self):
        pass

    def eval_declaration(self):
        pass

    def eval_asignation(self):
        pass