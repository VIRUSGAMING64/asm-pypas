class mem_Var:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class mem_Func:
    def __init__(self, name, args, code):
        self.name = name
        self.args = args
        self.code = code


class Memory:
    def __init__(self,memory_map = None , max_alloc=-1):
        self.mem = {} if memory_map is None else memory_map

    def alloc_var(self, addr,value):
        self.mem[addr] = mem_Var(
            addr, value
        )

    def query(self,addr):
        value = self.mem.get(addr,None)
        return value

    def alloc_func(self,addr, NoA, code):
        val = self.mem.get(addr,None)
        if val != None:
            raise "Overwrite addr"
        
        self.mem[addr] = mem_Func(addr,NoA, code)
        