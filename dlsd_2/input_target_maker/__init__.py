import inspect

def funcname():
    return inspect.stack()[1][3]