import errno
import os
from os import path

from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.output import GraphvizOutput

if os.environ.get('GENERATE_CALL_GRAPHS') is not None:
    _GENERATE_CALL_GRAPH = bool(os.environ['GENERATE_CALL_GRAPHS'])
else:
    _GENERATE_CALL_GRAPH = False

_CALL_GRAPHS_PATH = path.abspath(path.join(".", "calls"))

# Create Call diagrams folder
if _GENERATE_CALL_GRAPH:
    try:
        os.makedirs(_CALL_GRAPHS_PATH)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(_CALL_GRAPHS_PATH):
            pass
        else:
            raise

_call_graph_config = Config()
_call_graph_config.trace_filter = GlobbingFilter(exclude=[
    'pycallgraph.*'
])

def call_graph_ignore(*args):
    global _call_graph_config
    for exclude in args:
        if exclude not in _call_graph_config.trace_filter.exclude:
            _call_graph_config.trace_filter.exclude.append(exclude)

def generate_call_graph(func):
    """Generates Call Graph for the called function"""
    def wrapper(s, *args, **kwargs):
        if _GENERATE_CALL_GRAPH:
            caller_func = func.__name__
            if len(args) > 1:
                caller_func += "_" + "_".join(args[1:])
            with PyCallGraph(output=GraphvizOutput(output_file=path.join(_CALL_GRAPHS_PATH, "{0}.png".format(caller_func)),
                                                   output_format="png"), config=_call_graph_config):
                return func(s, *args, **kwargs)
        else:
            return func(s, *args, **kwargs)
    return wrapper