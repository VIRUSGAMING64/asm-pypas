from modules.utils import *
from .Expression import *
import json
import os
mem = Memory()

class IF: 
    err = []
    def __init__(self,linenumer ,decl, code = None):
        self.code = None

        if len(decl.tokens) != 2:
            raise Exception(f"invalid declaration at line [{linenumer+1}]")  
            
        self.cond = Expression(decl.tokens[1])
        self.code = code

    def Token(self):
        Token("__if__",CONDITION, self.code)

class func: 
    def __init__(self,start, lines):
        self.code   = None
        self.decl   = lines[start]
        self.i      = start
        self.novars = []
        self.declaration()

    def declaration(self):
        print("Hereee")
        if len(self.decl.tokens) < 4:
            raise Exception(f"invalid declaration at line [{self.i}]")

        print("Hereee")
        toks = self.decl.tokens
        novars = []
        for pointer in range(3, len(toks), 2):
            try:
                var = toks[pointer]
                comma = toks[pointer + 1]

                if comma.expr == ")":
                    if (pointer + 2 != len(toks)):
                        raise f"Invalid function declaration at line [{self.i}]"
                    break

                if comma.expr != ',' or var.type != VARIABLES:                
                    for i in toks:
                        print(i.expr, end = " ")
                    print(var.expr,comma.expr)
                    raise Exception(f"invalid token un function declaration [{self.i}]")
                
                novars.append(var.expr)       

            except Exception as e:
                raise e

        self.novars = novars

class Executor:
    def __init__(self,code = ""):
        self.code = code

    def func(self,start, lines):
        eofun,code = self.extract(start + 1, lines)
        fun = None
        try:
            fun = func(start,lines)
            fun.code = lines[start+1:eofun]
        except Exception as e:
            self.output["Errors"].append(str(e))
            print(e)
        
        return fun,eofun


    def control(self, start,lines):
        print(lines[start].expr)
        eoif,code = self.extract(start+1,lines)
        cond = None
        try:
            cond = IF(start,lines[start],code)
        except Exception as e:
            self.output["Errors"].append(str(e))
            
        print(start, eoif)
        assert eoif >= start
        return  cond,eoif


    def extract(self,start,lines):
        i = start
        structure = Token("__source_code__")
        structure.tokens = []

        while i < len(lines):
            line = lines[i]
            if line.tokens[0].expr == "if":
                cond,i = self.control(i,lines)
                if cond != None:
                    structure.tokens.append(cond.Token())
            
            elif line.tokens[0].expr == "while":
                LOOP(i,lines)
            
            elif line.tokens[0].expr == "func":
                func,i = self.func(i,lines)
                structure.tokens.append(func)
            else:
                structure.tokens.append(line)
            
            if line.tokens[0].expr == "end":
                return i,structure
                        
            i   += 1 

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
        print(self.code)
        self.code = self.code.replace("\t","  ")
        print(self.code)

        code = self.code.split("\n")


        lines = TokenizeSource(code,self.output)
        structure = self.extract(0,lines)

        
        
        
        
        self.output["result"] = "no syntaxis error"



        return self.output