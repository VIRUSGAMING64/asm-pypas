
from modules.web.core.utils import *
from modules.generic.utils import *
import logging
import modules.interpreter as interpreter


@app.route("/api/run", methods=["POST"])
def run():
    name, code, error = parse_code_payload()
    
    if error is not None:
        return error

    if name not in codes:
        return error_response(404, "code entry not found")

    logging.log(logging.DEBUG,"running code...")
    try:
        if code != codes.get(name, b""):
            codes[name] = code
            saver.save(name, code.decode())

        out = interpreter.ExecuteCode(code.decode())
        return out, 200
    
    except Exception as e:
        logging.exception(f"failed to run code [{str(e)}]")
        return error_response(500, "internal server error")
    
    
@app.route("/api/save", methods=["POST"])
def save(): 
    name, code, error = parse_code_payload()
    if error is not None:
        return error
    if name not in codes:
        return error_response(404, "code entry not found")

    try:
        if code != codes.get(name):
            codes[name] = code
            saver.save(name, code.decode("utf-8"))

        return {"status": "ok"}, 200
    except Exception:
        logging.exception("failed to save code")
        return error_response(500, "internal server error")


@app.route("/api/getcode", methods=["POST", "GET"])
def sendCode():
    name = flask.request.args.get("name", None)
    
    if not is_safe_code_name(name):
        return error_response(400, "invalid file name")

    cod = codes.get(name, b"")
    if isinstance(cod, bytes):
        cod = cod.decode()
    else:
        return {"status":"fail"},400
    
    return {"status":"ok","code":cod},200

@app.route("/api/initcodes")
def initcodes():
    names = []
    cods = []
    for name in os.listdir(CODES_DIR):
        if not is_safe_code_name(name):
            continue

        code = read(saver.resolve_path(name))

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

@app.route("/api/newcode")
def newcode():
    name = flask.request.args.get("name")
    if not is_safe_code_name(name):
        return error_response(400, "invalid file name")

    res = {
        "status":"ok",
        "code": ""        
    }
    codes[name] = b""
    return res,200

@app.route("/api/delcurr")
def delcode():
    file = flask.request.args.get("name")
    if not is_safe_code_name(file):
        return {"status":"fail"}, 403

    try:
        saver.delete(file)
        codes.pop(file, None)
    except Exception as e:
        logging.log(logging.DEBUG,e)
        return {"status":"fail"}, 405

    return {"status":"ok"} , 200
