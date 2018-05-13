import errno
from os import path
import os

# Controls If Call Graphs will be generated and where they will be saved
from tests import tools

GENERATE_CALL_GRAPHS = True
CALL_GRAPHS_PATH = path.abspath(path.join(".", "calls"))

# Create Call diagrams folder
if GENERATE_CALL_GRAPHS:
    try:
        os.makedirs(CALL_GRAPHS_PATH)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(CALL_GRAPHS_PATH):
            pass
        else:
            raise

def generate_call_graph(fn, *args, **kwargs):
    if GENERATE_CALL_GRAPHS:
        return tools.generate_call_graph(CALL_GRAPHS_PATH, fn, *args, **kwargs)
    else:
        return fn(*args, **kwargs)
