

class Var:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Func:
    def __init__(self, name, args, code):
        self.name = name
        self.args = args
        self.code = code


class Memory:
    def __init__(self,memory_map = {} , max_alloc=-1):
        self.mem = memory_map

    def alloc_var(self, addr):
        val = self.mem.get(addr,None)
        if val != None:
            raise "Overwrite addr"
        self.mem[addr] = Var(
            addr, 0
        )

    def query(self,addr):
        value = self.mem.get(addr,None)
        return value

    def alloc_func(self,addr, NoA, code):
        val = self.mem.get(addr,None)
        if val != None:
            raise "Overwrite addr"
        
        self.mem[addr] = {
            Func(addr,NoA, code)
        }