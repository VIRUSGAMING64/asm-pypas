from modules.interpreter.Tokens import *
from modules.generic.utils import *
from modules.interpreter.memory import *


class Expression:
    def __init__(self, expr = None):
        self.expr:str = expr
        self.type     = None

    def Token(self):
        self.expr = cleanStr(self.expr)
        res = Tokenize(self.expr)
        return Token(self.expr, LINE, res)
    
    def __dict__(self):
        return {
            "expr":self.expr,
            "type":self.type
        }
    
    def evalstr(self):
        toks    = self.Token()
        return self.evalTokens(toks)

    def evalTokens(self,toks):
        nums    = []
        oper    = []
        unary   = True 

        for elem in toks.tokens:

            if elem.expr == "(":
                oper.append(elem)
                unary = True
            
            elif elem.expr == ")":
                while oper[-1].expr != "(":
                    a = nums.pop()
                    opp = oper.pop()

                    if opp.data.get("neg", False):
                        nums.append(Token(UnaryOP(Token(a, NUMBER), opp),BOLEAN))
                        continue

                    b = nums.pop()
                    n = process_op(a, b, opp)
                    nums.append(Token(n, NUMBER))
                
                oper.pop()
                unary = False


            elif is_operator(elem.expr):
                if unary and is_unary(elem.expr):
                    elem.data["neg"] = True
                
                while (len(oper)>0 and (
                        ((getPrio(oper[-1]) >= getPrio(elem)) and (elem.data.get("neg",False) >= 0)) or
                        (elem.data.get("neg",False) < 0 and ((getPrio(oper[-1])) >= getPrio(elem)))
                    )):
                    
                    a = nums.pop()
                    opp = oper.pop()
                    if opp.data.get("neg", False):
                        nums.append(
                            Token(UnaryOP(Token(a, NUMBER), opp), NUMBER)
                        )
                        continue

                    b = nums.pop()        
                    nums.append(Token(process_op(a, b , opp), NUMBER))


                unary = True
                oper.append(elem)
            
            
            else:
                unary = False
                nums.append(elem)


        while len(oper):
            a = nums.pop()
            opp = oper.pop()
            if opp.data.get("neg", False):
                nums.append(Token(UnaryOP(Token(a, NUMBER), opp),BOLEAN))
                continue

            b = nums.pop()
            n = process_op(a, b, opp)
            nums.append(Token(n, NUMBER))
    
        print(nums, oper)
        return nums,oper


def TokenizeSource(code,output):
        lines = []
        p = 0
        for line in code:
            p +=1
            if line == "": 
                continue
            
            ex = Expression(line)
            print("-" * 8)
            line = ex.Token()
            line.put("line", p)
            lines.append(line)
            for j in range(len(line.tokens)):
                if line.tokens[j].expr == "//":
                    line.tokens[j].type = COMMENT
                    line.tokens[j].tokens = line.tokens[j+1:]
                    del line.tokens[j+1:]
                    break

                if line.tokens[j].type == KEYWORD and j != 0:
                    output["Errors"].append(f"keyword not in the start of line [{p}]")
                    break

            for j in line.tokens:
                if j.type == INVALID:
                    output["Errors"].append(f"invalid token at line: {p}")
                print(j.type,j.expr)
        
        return lines