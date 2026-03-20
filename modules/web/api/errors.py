
from modules.web.core.config import *
from modules.web.core.utils import *

@app.errorhandler(413)
def payload_too_large():
    return error_response(400, f"payload too large (max {MAX_CODE_BYTES} bytes for code)")


