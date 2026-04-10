from modules.interpreter.Exceptions import *
from modules.interpreter.t_statics import *
from modules.interpreter.Tokens import Token
from modules.generic.utils import *
import modules.interpreter.debug as debug
from modules.interpreter.memory import *

class ExprParser:
    def __init__(self, memory:Memory, out, globmem = None):
        self.memory     = memory
        self.out        = out
        self.globmem    = globmem

    def evalTokens(self, toks):
        try:
            return self._evalTokens(toks)
        except Exception as e:
            print("ERROR:",e)
            line = None if isinstance(toks, list) else toks.data["line"]
            raise ArithmeticException(line, str(e))

    def funcat(self, i , tokens):
        opens = 1
        args = []
        arg = []
        for j in range(i+2, len(tokens)):
            if tokens[j].expr == "(":
                opens += 1
                arg.append(tokens[j])
            elif tokens[j].expr == ",":
                if opens == 1:    
                    args.append(arg)
                    arg = []
                else:
                    arg.append(tokens[j])
            elif tokens[j].expr == ")":
                opens -= 1
                arg.append(tokens[j])
            else:
                arg.append(tokens[j])

            if opens == 0:
                arg.pop()
                args.append(arg)
                return j,args
        
        raise Exception("Not closed function call !!")

    def extract_funcs_call(self,toks):
        tokens:list = toks.tokens
        for i in range(len(tokens)):
            if i + 1 >= len(tokens):
                break
            
            if tokens[i].type == VARIABLES and tokens[i + 1].expr == "(":
                eofc,args = self.funcat(i,tokens)
                if eofc == None:
                    raise Exception("Func call not closed")
                func = Token("__func__", FUNCCALL, []) 
                func.data["args"] = []
                func.data["name"] = tokens[i].expr
                for arg in args:
                    func.data["args"].append(arg)
                del tokens[i : eofc + 1]
                tokens.insert(i, func)

    def call(self, elem, args:list, mem:Memory):

        m_func = mem.query(elem.data["name"])
        if m_func.type != FUNC:
            raise InterpreterMemoryError(f"No function at addr [{m_func.name}]")

        code = m_func.code      

        if len(m_func.args) != len(args):
            raise CallFuncException(elem)
        

        if code == BUILTIN:
            name = m_func.name
            ret = in_builtin.__builtins_calls__[name](*args)
            if ret == None:
                ret = 0
            return Token(ret, GetType(ret))


        newmem = Memory() 
        #* Aqui se crea un nuevo memory  segment para esta llamada
        #* en el for se declaran en ese nuevo segmento las variables que se pasana como argumento
        for i,arg_name in enumerate(m_func.args):
            if isinstance(args[i], mem_Func | mem_Var):
                newmem[arg_name] = args[i].copy()
                newmem[arg_name].name = arg_name
                continue
        
            args[i] = Token(args[i], GetType(args[i]))
            args[i].data["name"] = arg_name
            newmem.alloc_var(
                arg_name, args[i].expr, True, False
            )
        
        #* en este for las variables globales se pasan por referencia a la siguiente llamada de funcion
        for addr in mem.mem:
            if mem.mem[addr].isglob == False:
                continue
            newmem.mem[addr] = mem.mem[addr] #* Aqui lo que se hace es coger la referencia directa a las globales   
           
        ret = Evaluator(code, 0 , self.out, newmem, True).run()       
        ret = Token(ret, GetType(ret))
        return ret 

    def _evalTokens(self,ev_tokens):
        toks = ev_tokens.copy()
        if isinstance(toks, list):
            toks = Token(None, LINE , toks)
        nums    = []
        oper    = []
        unary   = True 

        self.extract_funcs_call(toks)
        for to in toks.tokens:
            print(to.expr)

        for i in range(len(toks.tokens)):
            if toks.tokens[i].type == FUNCCALL:
                args = []
                for arg in toks.tokens[i].data["args"]:
                    if arg == []:
                        continue
                    out = self.evalTokens(arg)
                    if len(out[0]) != 1 or len(out[1]) != 0:
                        print("here ?")
                        raise InterpreterException(toks) 
                    arg = out[0][0].expr
                    args.append(arg)
                toks.tokens[i] = self.call(toks.tokens[i], args, self.memory)

        for elem in toks.tokens:
            if elem.type == COMMENT:
                continue
            
            if elem.type == VARIABLES:
                elem.expr = self.memory.query(elem.data["name"])
            
            if elem.expr == "(":
                oper.append(elem)
                unary = True
            
            elif elem.expr == ")":
                while oper[-1].expr != "(":
                    self.process(nums, oper)
                
                oper.pop()
                unary = False

            elif is_operator(elem.expr):
                if unary and is_unary(elem.expr):
                    elem.data["neg"] = True
                
                while (len(oper)>0 and (
                        ((getPrio(oper[-1]) >= getPrio(elem)) and (elem.data.get("neg",False) >= 0)) or
                        (elem.data.get("neg",False) < 0 and ((getPrio(oper[-1])) >= getPrio(elem)))
                    )):
                    
                    self.process(nums, oper)

                unary = True
                oper.append(elem)
            else:
                unary = False
                nums.append(elem)
        
        while len(oper):
            self.process(nums,oper)


        if len(nums) != 1:
            for i in nums:
                print(i.expr)
            raise ExpresionException(toks)

        return nums,oper

    def process(self, nums, oper):
        a = nums.pop()
        opp = oper.pop()
        if opp.data.get("neg", False):
            res = UnaryOP(a,  opp)
            nums.append(
                Token( res, GetType(res))
            )
            return
        b = nums.pop()        
        n = process_op(a, b, opp, self.memory)
        if n == None:
            #* se esta haciendo una asignacion de valor 
            n = a

        nums.append(Token(n, GetType(n)))


class Evaluator:
    def __init__(self,structure:Token = None, start = None, output = {},memory = None, isfunc = False):
        self.pos        = start if start is not None else 0
        self.out        = output
        self.exceptions = []
        self.Tree       = structure
        self.memory     = memory
        self.isfunc     = isfunc
        if self.Tree is None:
            raise Exception("The source tree is None")
        
    def run(self):
        code, ret   = self.step()
        while code != RETURNING:
            if len(self.out['Errors']) >= 1:
                break
            li = self.Tree.tokens[self.pos].data.get("line", "UNKNOW")
            code, ret = self.step()

            print("Excecuted line:", li)
        
        #* esto es para debug solamente
        if debug.DEBUG:
            print("---" * 3, "memory audit", "---" * 3)
            audit = debug.audit_memory(self.memory)
            print(audit)
            self.out["result"] = audit
        return ret

    def step(self):
        try:
            retcode,out = self.execute(self.Tree.tokens[self.pos],self.memory)
            if retcode == INVALID:
                return INVALID, None
            if retcode != JUMPED:
                self.pos += 1
            if self.pos >= len(self.Tree.tokens):
                return RETURNING, 0 #! valor dafault para retorno de una funcion
            elif retcode == RETURNING:
                return retcode,out
        except InterpreterMemoryError as e:
            self.out["Errors"].append(e.GetError())
            return INVALID,None
        return EMPTY, out

    def execute(self, line, mem):
        if line.tokens == None:
            print("debug none: ",line.expr)
            return EMPTY,None
        
        if len(line.tokens) == 0:
            print("debug zero: ",line.expr)
            return EMPTY,None
        
        if line.type == CONDITION:
            return self.execute_condition(line, mem.copy())
        
        elif line.tokens[0].expr == 'var':
            try:
                self.variable_declaration(line,mem=mem)
            except DeclarationException as e:
                self.out["Errors"].append(e.GetError())
        
        elif line.tokens[0].type == LABEL:
            return EMPTY,None
        
        elif line.tokens[0].expr == "goto":
            try:
                return self.find_label(line, line.tokens[1].expr),None
            except GotoException as e:
                self.out["Errors"].append(e.GetError())
        
        elif line.tokens[0].expr == "ret":
            to_Eval = line.tokens[1:]
            value,err = ExprParser(mem,self.out).evalTokens(to_Eval)        
            if len(err) > 0 or len(value) != 1:
                raise InterpreterException("Return funcion value error")
            return RETURNING,value[0].expr            
        else:
            print("debug line: ",line.expr)
            return self.run_line(line, mem)
        
        return EMPTY,None
        
    def run_line(self, line , mem):
        if line.type ==  FUNC:
            print("debug func: ", line.expr)
            return EMPTY, None #* esto es para no evaluar las declaraciones de funciones 
        #* ya que la funcion en si es un token que se intenta evaluar
        try:
            try: #* esto es asi porque primero se intentan usar las variables globales en la linea
                ExprParser(self.memory,self.out).evalTokens(line)
            except InterpreterMemoryError as e:
                print("global error: ",e)
                ExprParser(mem,self.out).evalTokens(line)
        except InterpreterException as e:
            self.out["Errors"].append(e.GetError())
            return INVALID,None
        return EMPTY, None

    def find_label(self,line , name):
        name += ":"
        pos = -1
        for i in range(len(self.Tree.tokens)):
            pos += 1
            if self.Tree.tokens[i].expr == name:
                return self.jump(pos),None
        raise GotoException(line)
    
    def execute_condition(self, line, mem):       
        cond = line.data["condition"]
        value,err = ExprParser(mem,self.out).evalTokens(cond)
        if len(value) != 1 or len(err) != 0:
            raise Exception("Invalid condition")
        
        if not value[0].expr:
            newpos =self.pos + line.data["dx"]
            return self.jump(newpos),None 
        
        return EMPTY, None

    def jump(self, pos):
        self.pos = pos
        return JUMPED

    def variable_declaration(self, line, mem:Memory):
        try:
            try:
                if len(line.tokens) < 3 or line.tokens[1].type != VARIABLES or line.tokens[2].expr != "=":
                    raise DeclarationException(VARIABLES, line, [])
            
                value,err = ExprParser( mem, self.out).evalTokens(line.tokens[3:])
            
            except DeclarationException as e:
                if isinstance(e, DeclarationException):
                    self.out["Errors"].append(e.GetError())
                return INVALID,None
            
            try:
                value = value[0].expr
                mem.alloc_var(line.tokens[1].data["name"],value,False, isglob = not self.isfunc)
            except InterpreterMemoryError as e:
                self.out["Errors"].append(e.GetError())
                return INVALID,None

        except InterpreterException as e:
            if isinstance(e, ArithmeticException):
                e.line = line
                self.out["Errors"].append(e.GetError())
                return INVALID,None
            elif isinstance(e, InterpreterMemoryError):
                e.line = line
                self.out["Errors"].append(e.GetError())
                return INVALID, None
            
            self.out["Errors"].append(f"python exception at line [{line.data["line"]}]:[{str(e)}]")
        
        return VARIABLES,None