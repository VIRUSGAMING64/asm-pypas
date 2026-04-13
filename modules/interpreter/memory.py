from modules.interpreter.Exceptions import *
from modules.interpreter.statics_values import *
import modules.interpreter.builtin as in_builtin


class mem_Var:
    def __init__(self, name, value, isglob):
        self.name  = name
        self.value = value
        self.type  = VARIABLES
        self.isglob = isglob

    def copy(self):
        return mem_Var(self.name, self.value, self.isglob)

class mem_Func:
    def __init__(self, name, args, code):
        self.name  = name
        self.args  = args
        self.code  = code
        self.value = f"function at [{name}]"
        self.type  = FUNC 
        self.isglob = True #* las funciones siempre se declaran globales en donde esten

    def copy(self):
        return mem_Func(self.name, self.args.copy(), self.code.copy())



class Memory:
    def __init__(self,memory_map = None , max_alloc=-1, skip_builtins=False):
        self.mem = {} if memory_map is None else memory_map
        self.max_alloc = max_alloc
        if not skip_builtins:
            self.__init_builtins()


    def __setitem__(self, key, value):
        self.mem[key] = value

    def __getitem__(self, key):
        return self.mem.__getitem__(key)

    def __init_builtins(self):
        for name, args in in_builtin.__builtins_funcs__:
            try:
                self.alloc_func(name, args, BUILTIN)
                self.mem[name].isglob = False
            except Exception  as e:
                print("ya allocted: ",e)
                
    def partialcopy(self):
        newmem = {}
        for addr in self.mem:
            newmem[addr] = self.mem[addr] 
            #*aqui solo se hace una referencia las que ya existen
            #*las nuevas que se creen no modifican la anterior memoria
        return Memory(newmem, -1 , True)

    def copy(self):
        return Memory(self.mem.copy(), self.max_alloc, skip_builtins=True)

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
            if var == None:
                raise InterpreterMemoryError(f"Addr [{addr}] not allocated")
            if isinstance(var , mem_Func):
                return var
            value = var.value
            return value
        except:
            raise InterpreterMemoryError(F"Addr of variable [{addr}] is invalid or variable not declared")

    def alloc_func(self,addr, args, code):
        val = self.mem.get(addr,None)
        if val != None:
            print(val.name)
            raise InterpreterMemoryError(f"Overwrite addr [{addr}]")
        
        self.mem[addr] = mem_Func(addr,args, code)
        