import os
import flask
from modules.web.core.saver import *


CODES_DIR                        = os.path.realpath("./codes")
saver                            = CodeSaver(CODES_DIR)
app                              = flask.Flask("app")
ROOT                             = os.path.realpath("./gui/guihtml")
MAX_CODE_BYTES                   = 1024**2 * 128
MAX_JSON_PAYLOAD_BYTES           = MAX_CODE_BYTES + 1024
app.config["MAX_CONTENT_LENGTH"] = MAX_JSON_PAYLOAD_BYTES
codes                            = {}