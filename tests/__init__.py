import os

from tests.tools.callgraph import enable_call_graph

if os.environ.get('GENERATE_CALL_GRAPHS') is not None:
    GENERATE_CALL_GRAPHS = bool(os.environ['GENERATE_CALL_GRAPHS'])
else:
    GENERATE_CALL_GRAPHS = False

enable_call_graph(enabled=GENERATE_CALL_GRAPHS)
