from modules.interpreter.Exceptions import *
class mem_Var:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class mem_Func:
    def __init__(self, name, args, code):
        self.name = name
        self.args = args
        self.code = code
        self.value = f"function at [{name}]"

class Memory:
    def __init__(self,memory_map = None , max_alloc=-1):
        self.mem = {} if memory_map is None else memory_map
        self.max_alloc = max_alloc

    def copy(self):
        return Memory(self.mem.copy(), self.max_alloc)

    def alloc_var(self, addr,value):
        val = self.mem.get(addr,None)
        if val != None:
            raise InterpreterMemoryError(f"Overwrite addr [{addr}]")
        
        self.mem[addr] = mem_Var(
            addr, value
        )

    def Put(self, addr, value):
        val = self.mem.get(addr, None)
        if val == None:
            raise InterpreterMemoryError(f"Address not allocated [{addr}]")
        
        self.mem[addr] = mem_Var(addr, value)

    def query(self,addr):
        try:
            value = self.mem.get(addr,None).value
            return value
        except:
            raise InterpreterMemoryError(F"Addr of variable [{addr}] is invalid or variable not declared")

    def alloc_func(self,addr, NoA, code):
        val = self.mem.get(addr,None)
        if val != None:
            raise InterpreterMemoryError(f"Overwrite addr [{addr}]")
        
        self.mem[addr] = mem_Func(addr,NoA, code)
        