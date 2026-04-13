from modules.generic.utils import *
from modules.interpreter.Lexer import *
from modules.interpreter.ExprParser import *
import json
import modules.interpreter.debug as debug
import os
from .structures import *
import logging
from modules.interpreter.utils import *

def ExecuteCode(code):
    if not isinstance(code, str | dict):
        return {
            "Errors": ["code is invalid"],
            "result": ""
        }
    
    memory = Memory()
    output = {
        "Errors": [],
        "result":""
        }
    struct = None

    if isinstance(code,dict):
        struct = dict2Token(code)

    elif isinstance(code, str):
        lines    = Lexer(code, output).TokenizeSource()
        s,struct = extract(output, memory, 0 , lines)

    if output["Errors"] == []:
        for i in struct.tokens:
            print("debug:",i.expr, i.data.get("name", None))  
        code, res = Evaluator(struct, None, output, memory).run()
        
    logging.log(logging.DEBUG,memory.mem)


    return output