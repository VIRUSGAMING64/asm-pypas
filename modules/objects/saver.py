import os
class CodeSaver:
    def __init__(self,path):
        self.path = path
    
    def save(self, name, code:str):
        f = open(os.path.join(self.path + name), "wb")
        f.write(code.encode())
        f.close()
    
    def load(self,name):
        f = open(os.path.join(self.path + name), "r")
        data=f.read(2**30)
        f.close()
        return data