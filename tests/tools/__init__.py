import inspect
from os import path

from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.output import GraphvizOutput


call_graph_config = Config()
call_graph_config.trace_filter = GlobbingFilter(exclude=[
    'pycallgraph.*',
], )


def generate_call_graph(graph_path, func, *args, **kwargs):
    """Generates Call Graph for the called function"""
    caller_func = inspect.stack()[1][3]
    graphviz = GraphvizOutput(output_file=path.join(graph_path, "{0}.png".format(caller_func)))
    with PyCallGraph(output=graphviz, config=call_graph_config):
        return func(*args, **kwargs)
