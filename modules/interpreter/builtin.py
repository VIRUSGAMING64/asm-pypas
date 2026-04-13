import os
import time as pytime
import random
"""
source of __builtin__ functions
"""


def _time():
    return pytime.time_ns()

def _sleep(ms):
    return pytime.sleep(ms / 1000) 

def _getcwd():
    return os.getcwd()

def _random(a, b):
    return random.randint(a, b)

__builtins_funcs__ = [
    [
        "_time", []
    ],
    [
        "_sleep", ["ms"]
    ],
    [
        "_getcwd", []
    ],
    [
        "_random", ["a", "b"]
    ]
]

__builtins_calls__ = {
    "_time" : _time,
    "_getcwd": _getcwd,
    "_sleep" : _sleep,
    "_random": _random
}
