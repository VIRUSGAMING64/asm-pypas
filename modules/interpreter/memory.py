from modules.interpreter.Exceptions import *
from modules.interpreter.t_statics import *
class mem_Var:
    def __init__(self, name, value, isglob):
        self.name  = name
        self.value = value
        self.type  = VARIABLES
        self.isglob = isglob

class mem_Func:
    def __init__(self, name, args, code):
        self.name  = name
        self.args  = args
        self.code  = code
        self.value = f"function at [{name}]"
        self.type  = FUNC 
        self.isglob = True #* las funciones siempre se declaran globales en donde esten

class Memory:
    def __init__(self,memory_map = None , max_alloc=-1):
        self.mem = {} if memory_map is None else memory_map
        self.max_alloc = max_alloc

    def copy(self):
        return Memory(self.mem.copy(), self.max_alloc)

    def alloc_var(self, addr,value, overwrite = False, isglob = True):
        val = self.mem.get(addr,None)

        if not overwrite and val != None:
            raise InterpreterMemoryError(f"Overwrite addr [{addr}]")
        
        self.mem[addr] = mem_Var(
            addr, value, isglob
        )

    def Put(self, addr, value):
        val = self.mem.get(addr, None)
        if val == None:
            raise InterpreterMemoryError(f"Address not allocated [{addr}]")
        
        self.mem[addr].value=value

    def query(self,addr):
        try:
            var = self.mem.get(addr)
            if isinstance(var , mem_Func):
                return var
            value = var.value
            return value
        except:
            raise InterpreterMemoryError(F"Addr of variable [{addr}] is invalid or variable not declared")

    def alloc_func(self,addr, args, code):
        val = self.mem.get(addr,None)
        if val != None:
            raise InterpreterMemoryError(f"Overwrite addr [{addr}]")
        
        self.mem[addr] = mem_Func(addr,args, code)
        