from modules.generic.utils import *
from modules.interpreter.Expression import *
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

        structure = None
        if isinstance(self.code,dict):
            structure = dict2Token(self.code)

        elif isinstance(self.code, str):
            self.output = {
                "Errors": [],
                "result":""
            }
            self.code = self.code.replace("\t","  ")
            self.code = self.code.replace("\r","  ")
            code = self.code.split("\n")
            lines = TokenizeSource(code,self.output)
            s,structure = extract(self.output, self.mem, 0 , lines)

        if self.output["Errors"] == []:
            res = Evaluator(structure, None, self.output, self.mem).run()
            
        logging.log(logging.DEBUG,self.mem.mem)


        return self.output