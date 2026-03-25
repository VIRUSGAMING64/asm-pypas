import flask
import os
from modules.web.core.config import *
from modules.web.core.utils import *
import logging
from modules.generic.utils import *
#init of app endpoint and errors ej:(404)
from modules.web.api.endpoints import *
from modules.web.core.errors import *

for name in os.listdir(CODES_DIR):
    data = read(saver.resolve_path(name))
    if data == b"":
        saver.delete(name)
        continue

    codes[name] = data


@app.route("/")
def main():
    return response(ROOT+"/html/index.html")

@app.route("/api")
def api():
    return response(ROOT + "/html/api.html")


@app.route('/gui/<path:subpath>')
def show_subpath(subpath):

    try:
        safe_path = CodeSaver(ROOT).resolve_path(subpath) 
    except Exception as e:
        logging.log(logging.DEBUG, f"403 at [{subpath}]")
        return error_response(403, "Access denied")
    
    if not os.path.isfile(safe_path):
        return error_response(404, "file not found")
    
    return response(safe_path)
