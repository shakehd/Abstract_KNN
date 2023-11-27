from scipy.sparse._base import issparse as issparse
from scipy.sparse._csr import csr_matrix as csr_matrix
from typing import Any

__test__: dict

class MaximumFlowResult:
    def __init__(self, *args, **kwargs) -> None: ...

def maximum_flow(csgraph, source, sink) -> Any: ...
