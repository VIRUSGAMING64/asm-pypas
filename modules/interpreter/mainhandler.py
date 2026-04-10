from modules.generic.utils import *
from modules.interpreter.Lexer import *
from modules.interpreter.ExprParser import *
import json
import modules.interpreter.debug as debug
import os
from .structures import *
import logging
from modules.interpreter.utils import *

class MainHandler:
    def __init__(self,code = "", memory = None):
        self.code = code
        self.mem = Memory() if memory is None else memory

    def run(self):
        if not isinstance(self.code, str | dict):
            return {
                "Errors": ["code is invalid"],
                "result": ""
            }

        struct = None
        if isinstance(self.code,dict):
            struct = dict2Token(self.code)

        elif isinstance(self.code, str):
            self.output = {
                "Errors": [],
                "result":""
            }
            lines    = Lexer(self.code, self.output).TokenizeSource()
            s,struct = extract(self.output, self.mem, 0 , lines)

        if self.output["Errors"] == []:
            for i in struct.tokens:
                print("debug:",i.expr, i.data.get("name", None))  
            res = Evaluator(struct, None, self.output, self.mem).run()
            
        logging.log(logging.DEBUG,self.mem.mem)


        return self.output