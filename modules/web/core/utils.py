from modules.web.core.config import *
from modules.web.core.saver import *

def error_response(status_code, message):
    return {"status": "fail", "message": message}, status_code


def is_safe_code_name(name):
    if not isinstance(name, str):
        return False

        
    name = name.strip()
    if name == "" or name in {".", ".."}:
        return False

    if "/" in name or "\\" in name:
        return False

    saver.resolve_path(name)


    return True


def parse_code_payload():
    content_length = flask.request.content_length
    if content_length is not None and content_length > MAX_JSON_PAYLOAD_BYTES:
        return None, None, error_response(400, f"payload too large (max {MAX_CODE_BYTES} bytes for code)")

    payload = flask.request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, None, error_response(400, "invalid JSON body")

    name = payload.get("name")
    code = payload.get("code")

    if not isinstance(name, str) or name.strip() == "":
        return None, None, error_response(400, "field 'name' is required")
    if not is_safe_code_name(name):
        return None, None, error_response(400, "invalid file name")
    if not isinstance(code, str):
        return None, None, error_response(400, "field 'code' must be a string")

    code_bytes = code.encode("utf-8")
    if len(code_bytes) > MAX_CODE_BYTES:
        return None, None, error_response(400, f"payload too large (max {MAX_CODE_BYTES} bytes for code)")
    return name, code_bytes, None
