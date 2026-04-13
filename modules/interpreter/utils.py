
from modules.interpreter.structures import *

def ex_func(output, memory,start, lines):
    eofun,code = extract(output,memory,start + 1, lines)
    try:
        fun = None
        fun = FUNCS(start,lines)
        fun.code = code
    except Exception as e:
        output["Errors"].append(str(e))
        logging.log(logging.DEBUG,e)
    
    return fun,eofun

def control(output, memory,start,lines):
    logging.log(logging.DEBUG,lines[start].expr)
    dx,code = extract(output, memory,start+1,lines)
    cond = None
    try:
        cond = IF(start,lines[start],code)
    except Exception as e:
        output["Errors"].append(str(e))
        
    logging.log(logging.DEBUG,start, dx)
    return  cond,dx

def loop(output, memory,start,lines):
    logging.log(logging.DEBUG,lines[start].expr)
    dx,code = extract(output, memory,start+1,lines)
    Loop = None
    try:
        Loop = Token(
            lines[start], LOOP, code.tokens, {"line": start, "condition": lines[start].tokens[1:]}
        )
    except Exception as e:
        output["Errors"].append(str(e))
        
    logging.log(logging.DEBUG,start, dx)
    return  Loop,dx

def extract(output,memory,start,lines):
    i = start
    structure = Token("__source_code__", NIL, [], {})
    
    while i < len(lines):
        line = lines[i]

        if len(line.tokens) == 0:
            logging.log(logging.DEBUG,line.tokens, line.expr)
            i+=1
            continue
        elif line.tokens[0].expr == "if":
            cond,dx = control(output,memory,i,lines)
            if cond != None:
                tk = cond.Token()
                tk.data["dx"] = dx-i
                i = dx
                structure.tokens.append(tk)
        elif line.tokens[0].expr == "while":
            
            Loop,dx = loop(output,memory,i,lines)
            if Loop != None:
                Loop.data["dx"] = dx-i
                i = dx
                structure.tokens.append(Loop)
            
        elif line.tokens[0].expr == "func":
            func,i = ex_func(output,memory,i,lines)
            try:
                if func != None:
                    memory.alloc_func(func.name, func.novars, func.code)
                    structure.tokens.append(func.Token())
            except InterpreterException as e:
                logging.log(logging.DEBUG,e)
                output["Errors"].append(f"Overwriting [{func.name}] function address at line [{line.get('line','unknow')}]")
        else:
            logging.log(logging.DEBUG,"added",line.expr)
            structure.tokens.append(line)   

        if line.tokens[0].expr == "end":
            if start != 0:
                return i,structure
            else:
                output["Errors"].append(f"invalid end position at line [{line.data["line"]}]")
        i += 1 

    if start != 0:
        output["Errors"].append(f"Not closed structure at line [{start}]")
    
    return i,structure 
