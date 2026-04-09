import os
import time as pytime
"""
source of __builtin__ functions
"""


def _time():
    """return time in ns"""
    return pytime.time_ns()

def _sleep(ms):
    return pytime.sleep(ms / 1000) 

def _getcwd():
    return os.getcwd()

__builtins_funcs__ = [
    ["_time", []],
    ["_sleep", ["ms"]],
    ["_getcwd", []]
]

__builtins_calls__ = {
    "_time" : _time,
    "_getcwd": _getcwd,
    "_sleep" : _sleep
}
