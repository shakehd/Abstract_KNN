from .bvls import bvls as bvls
from .common import compute_grad as compute_grad, in_bounds as in_bounds
from .trf_linear import trf_linear as trf_linear
from _typeshed import Incomplete
from scipy.optimize import OptimizeResult as OptimizeResult
from scipy.optimize._minimize import Bounds as Bounds
from scipy.sparse import csr_matrix as csr_matrix, issparse as issparse
from scipy.sparse.linalg import LinearOperator as LinearOperator, lsmr as lsmr

def prepare_bounds(bounds, n): ...

TERMINATION_MESSAGES: Incomplete

def lsq_linear(A, b, bounds=..., method: str = ..., tol: float = ..., lsq_solver: Incomplete | None = ..., lsmr_tol: Incomplete | None = ..., max_iter: Incomplete | None = ..., verbose: int = ..., *, lsmr_maxiter: Incomplete | None = ...): ...
