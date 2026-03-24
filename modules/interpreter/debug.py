
from .Tokens import Token

def dst(structure:Token,prof = 0):
    print(prof * " ",end = "")
    print(structure.expr)
    if structure.tokens != None:
        print(len(structure.tokens))
    assert(isinstance(structure.expr,str))
    if structure.tokens == None:
        return
    
    print("-"*40)   

    
    for sub in structure.tokens:
        dst(sub, prof+1)

    

def audit_memory(mem):
    for addr in mem.mem:
        print(addr, mem.query(addr))