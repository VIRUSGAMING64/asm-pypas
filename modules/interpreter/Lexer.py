from modules.interpreter.Tokens import *
from modules.generic.utils import *
from modules.interpreter.memory import *
from modules.interpreter.Exceptions import *
import time

class Lexer:

    def __init__(self, code,output):
        code = code.replace("\t","  ")
        code = code.replace("\r","  ")
        code = code.split("\n")
        self.code = code
        self.output = output

    def Tokenize(self, expr: str) -> list[Token]:
        pos = 0
        act_tok = ""
        tokens = []
        start_str = None
        in_str = False
        while pos <= len(expr):

            if (pos < len(expr)) and ((not expr[pos] in operators) or in_str):
                act_tok += expr[pos]

                if start_str == None and expr[pos] in ["\"", "\'"]:
                    in_str = not in_str
                    start_str = expr[pos]
                
                elif expr[pos] == start_str:
                    in_str = not in_str
                    start_str = None

            else:
                dis = -1        
                act_tok = cleanStr(act_tok)
                tokens.append(
                    Token(act_tok,NIL)
                  )

                if pos < len(expr):            
                    dis -= 1
                
                p = False
                if act_tok == "":
                    tokens.pop()
                    p = True

                if dis == -2:
                    tokens.append(Token(expr[pos], OPERATION))
                    if pos + 1 != len(expr) and expr[pos] + expr[pos + 1] in operators:
                        tokens[len(tokens) - 1].expr += expr[pos + 1]
                        pos += 1
            
                if p: 
                    pos += 1
                    continue
            
                t_token = tokens[len(tokens) + dis]
                le = len(t_token.expr)
                
                t_token.data["name"] = t_token.expr

                if t_token.expr.isnumeric():
                    t_token.type = NUMBER
                    t_token.expr = int(t_token.expr)
                elif t_token.expr.startswith("\"") and t_token.expr.endswith("\"") and le > 1:
                    t_token.type = STRING
                    t_token.expr = t_token.expr.removeprefix("\"").removesuffix("\"")
                elif t_token.expr.startswith("'") and t_token.expr.endswith("'") and le > 1:
                    t_token.type = STRING
                    t_token.expr = t_token.expr.removeprefix("\'").removesuffix("\'")
                elif t_token.isKeyword():
                    t_token.type = KEYWORD
                elif t_token.isLabel():
                    t_token.type = LABEL
                elif t_token.VarName():
                    t_token.type = VARIABLES            
                act_tok = ""
            pos += 1
            
        line_tokens = []

        for i in range(len(tokens)):
            line:Token = tokens[i]
            if line.type == NIL:
                splited_tokens = self.getErrs(line.expr)
                for t in splited_tokens:
                    if t == []:
                        continue
                    line_tokens.append(t[0])        
            else:
                line_tokens.append(line)      

        return line_tokens

        
    def getErrs(self,  expr):
        expr = expr.split(' ')
        if len(expr) == 1:
            return [[Token(expr[0],INVALID)]]
        arr = []
        for x in expr:
            arr.append(self.Tokenize(x))

        return arr

    def str2Token(self,expr):
        expr = cleanStr(expr)
        res = self.Tokenize(expr)
        return Token(expr, LINE, res)

    def TokenizeSource(self):
        lines = []
        p = 0
        for line in self.code:
            p += 1
            li = self.ProcessRawLine(line, p)
            lines.append(li)

        return lines


    def ProcessRawLine(self, line, p):
        if line == "": 
            return Token("", LINE, data = {"line": p})
        
        t_line = self.str2Token(line)
        print("debugeando: ",t_line.expr, t_line.data["name"])
        
        for j in range(len(t_line.tokens)):
            if t_line.tokens[j].expr == "//":
                t_line.tokens[j].type = COMMENT
                t_line.tokens[j].tokens = t_line.tokens[j+1:]
                del t_line.tokens[j+1:]
                break

            if t_line.tokens[j].type == KEYWORD and j != 0:
                self.output["Errors"].append(f"keyword not in the start of line [{p}]")
                break

        for j in t_line.tokens:
            if j.type == INVALID:
                self.output["Errors"].append(f"invalid token at line: {p}")

        t_line.put("line", p)
        
        return t_line