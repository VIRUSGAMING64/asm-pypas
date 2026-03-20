
from .Tokens import Token

def dst(structure:Token,prof = 0):
    print(prof * " ",end = "")
    print(structure.expr)
    assert(isinstance(structure.expr,str))
    if structure.tokens == None:
        return
    print("-"*40)   
    for i in structure.tokens:
        dst(i, prof+1)

    