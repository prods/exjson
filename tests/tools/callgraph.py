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


def generate_call_graph(fn, *args, **kwargs):
    if _GENERATE_CALL_GRAPH:
        return _generate_call_graph(_CALL_GRAPHS_PATH, fn, *args, **kwargs)
    else:
        return fn(*args, **kwargs)


call_graph_config = Config()
call_graph_config.trace_filter = GlobbingFilter(exclude=[
    'pycallgraph.*',
], )


def _generate_call_graph(graph_path, func, *args, **kwargs):
    """Generates Call Graph for the called function"""
    caller_func = "test_" + func.__name__
    if len(args) > 1:
        caller_func += "_" + "_".join(args[1:])
    with PyCallGraph(output=GraphvizOutput(output_file=path.join(graph_path, "{0}.png".format(caller_func)),
                                           output_format="png"), config=call_graph_config):
        return func(*args, **kwargs)
