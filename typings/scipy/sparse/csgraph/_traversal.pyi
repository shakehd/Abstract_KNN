from scipy.sparse.csgraph._tools import reconstruct_path as reconstruct_path
from scipy.sparse.csgraph._validation import validate_graph as validate_graph
from typing import Any

__test__: dict

def breadth_first_order(csgraph, i_start, directed=..., return_predecessors=...) -> Any: ...
def breadth_first_tree(*args, **kwargs): ...
def connected_components(csgraph, directed=..., connection=..., 
return_labels=...) -> Any: ...
def depth_first_order(csgraph, i_start, directed=..., return_predecessors=...) -> Any: ...
def depth_first_tree(*args, **kwargs): ...
