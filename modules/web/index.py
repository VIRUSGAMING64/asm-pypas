import flask
import os
from modules.web.core.config import *
from modules.web.core.utils import *
import logging
from modules.generic.utils import *
#init of app endpoint and errors ej:(404)
from modules.web.api.endpoints import *
from modules.web.api.errors import *




for name in os.listdir(CODES_DIR):
    data = read(saver.resolve_path(name))
    if data == b"":
        saver.delete(name)
        continue

    codes[name] = data


@app.route("/")
def main():
    return response(ROOT+"/index.html")


@app.route('/gui/<path:subpath>')
def show_subpath(subpath):
    if ".." in subpath:
        return "Access denied", 403
    return response(ROOT+"/"+subpath)
