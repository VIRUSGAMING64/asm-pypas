import flask
import os
from modules import *

os.makedirs("codes", exist_ok=True)
cods = os.listdir("codes")
codes = {}
for name in cods:
    data = read("codes/"+name)
    if data == b"":
        os.remove("codes/" + name)
        continue
    codes[name] = data


app   = flask.Flask("app")
ROOT  = os.path.realpath("./gui")
saver = CodeSaver("codes/")


@app.route("/run")
def run():
    code = flask.request.args.get("code", "")
    name = flask.request.args.get("name", "")
    logging.log(logging.DEBUG,"running code...")
    code = code.encode()
    if code != codes.get(name, b""):
        codes[name] = code
        saver.save(name,code.decode())

    exe = MainHandler(code.decode())
    out = exe.run()
    logging.log(logging.DEBUG,out)
    return out,200
    
    
@app.route("/save")
def save(): 
    code = flask.request.args.get("code", "")
    name = flask.request.args.get("name", "")
    code = code.encode()
    if code != codes.get(name):
        codes[name] = code
        saver.save(name,code.decode())

    return {"status":"ok"},200


@app.route("/getcode", methods=["POST"])
def sendCode():
    name = flask.request.args.get("name")
    logging.log(logging.DEBUG,name)
    cod = codes.get(name, b"")
    if isinstance(cod, bytes):
        cod = cod.decode()
    else:
        return {"status":"fail"},200
    
    return {"status":"ok","code":cod},200


@app.route("/")
def main():
    return response(ROOT+"/index.html")


@app.route('/gui/<path:subpath>')
def show_subpath(subpath):
    if ".." in subpath:
        return "Access denied", 403
    return response(ROOT+"/"+subpath)

@app.route("/getcodes")
def getcodes():
    name = flask.request.args.get("name", "")
    cod =codes.get(name, b"")
    if isinstance(cod, bytes):
        cod = cod.decode()
    else:
        return {"status" : "fail"}
    
    return {
        "status":"ok",
        "code"  : cod
    }

@app.route("/initcodes")
def initcodes():
    names = []
    cods = []
    for name in os.listdir("codes"):
        code = read("codes/"+name)
        if code == b"":
            continue
        
        cods.append(name)
        

    for name in cods:
        names.append(name)
    
    res = {
        "status" : "ok",
        "names": names
    }

    return res,200

@app.route("/newcode")
def newcode():
    name = flask.request.args.get("name")
    res = {
        "status":"ok",
        "code": ""        
    }
    codes[name] = b""
    return res,200

@app.route("/delcurr")
def delcode():
    file = flask.request.args.get("name")
    file = file.replace("..", "")
    try:
        os.remove(os.path.abspath("./codes/")+"/"+file)
    except Exception as e:
        logging.log(logging.DEBUG,e)
    return {"status":"ok"}

if __name__ == "__main__":
    app.run("0.0.0.0", 9000)