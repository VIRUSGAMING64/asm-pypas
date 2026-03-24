from modules.generic.utils import *
from .Expression import *
import json
import modules.interpreter.debug as debug
import os
from .structures import *
import logging

class MainHandler:
    def __init__(self,code = ""):
        self.code = code
        self.mem = Memory()

    def func(self,start, lines):
        eofun,code = self.extract(start + 1, lines)
        try:
            fun = None
            fun = FUNCS(start,lines)
            fun.code = code
        except Exception as e:
            self.output["Errors"].append(str(e))
            logging.log(logging.DEBUG,e)
        
        return fun,eofun


    def control(self, start,lines):
        logging.log(logging.DEBUG,lines[start].expr)
        eoif,code = self.extract(start+1,lines)
        cond = None
        try:
            cond = IF(start,lines[start],code)
        except Exception as e:
            self.output["Errors"].append(str(e))
            
        logging.log(logging.DEBUG,start, eoif)
        assert eoif >= start
        return  cond,eoif


    def extract(self,start,lines):
        i = start
        structure = Token("__source_code__")
        structure.tokens = []

        while i < len(lines):
            line = lines[i]
            if len(line.tokens) == 0:
                logging.log(logging.DEBUG,line.tokens, line.expr)
                i+=1
                continue

            elif line.tokens[0].expr == "if":
                cond,i = self.control(i,lines)
                if cond != None:
                    structure.tokens.append(cond.Token())

            elif line.tokens[0].expr == "func":
                func,i = self.func(i,lines)
                try:
                    if func != None:
                        self.mem.alloc_func(func.name, func.novars, func.code)
                        structure.tokens.append(func.Token())
                except Exception as e:
                    logging.log(logging.DEBUG,e)
                    self.output["Errors"].append(f"Overwriting function address [{line.get('line','unknow')}]")
            else:
                logging.log(logging.DEBUG,"added",line.expr)
                structure.tokens.append(line)   
            
            if line.tokens[0].expr == "end":
                return i,structure
                       
            i += 1 

        if start != 0:
            self.output["Errors"].append("Not closed structure")
        
        return i,structure 


    def run(self, code = None):
        
        if code != None:
            self.code = code

        self.output = {
            "Errors": [],
            "result":""
        }
        self.code = self.code.replace("\t","  ")
        self.code = self.code.replace("\r","  ")
        code = self.code.split("\n")
        lines = TokenizeSource(code,self.output)

        print(lines[0].expr)

        s,structure = self.extract(0,lines)
        if len(self.output["Errors"]) == 0:
            self.output["result"] = "no syntaxis error"
        else:
            self.output["result"] = "to many errors"
            
        if self.output["Errors"] == []:
            
            debug.dst(structure)
            Evaluator(structure, None, self.output, self.mem).run()
        
        logging.log(logging.DEBUG,self.mem.mem)


        return self.output