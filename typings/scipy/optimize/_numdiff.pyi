from ..sparse import coo_matrix as coo_matrix, csc_matrix as csc_matrix, csr_matrix as csr_matrix, find as find, issparse as issparse
from ._group_columns import group_dense as group_dense, group_sparse as group_sparse
from _typeshed import Incomplete
from scipy.sparse.linalg import LinearOperator as LinearOperator

def group_columns(A, order: int = ...): ...
def approx_derivative(fun, x0, method: str = ..., rel_step: Incomplete | None = ..., abs_step: Incomplete | None = ..., f0: Incomplete | None = ..., bounds=..., sparsity: Incomplete | None = ..., as_linear_operator: bool = ..., args=..., kwargs=...): ...
def check_derivative(fun, jac, x0, bounds=..., args=..., kwargs=...): ...
