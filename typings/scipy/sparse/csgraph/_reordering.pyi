from scipy.sparse._base import SparseEfficiencyWarning as SparseEfficiencyWarning, issparse as issparse
from scipy.sparse._csr import csr_matrix as csr_matrix
from scipy.sparse.csgraph._matching import maximum_bipartite_matching as maximum_bipartite_matching
from typing import Any, overload

__test__: dict

def reverse_cuthill_mckee(graph, symmetric_mode=...) -> Any: ...
@overload
def structural_rank(graph) -> Any: ...
@overload
def structural_rank(graph) -> Any: ...
