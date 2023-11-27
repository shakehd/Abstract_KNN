from .base import DenseOutput as DenseOutput, OdeSolver as OdeSolver
from .common import EPS as EPS, norm as norm, num_jac as num_jac, select_initial_step as select_initial_step, validate_first_step as validate_first_step, validate_max_step as validate_max_step, validate_tol as validate_tol, warn_extraneous as warn_extraneous
from _typeshed import Incomplete
from scipy.linalg import lu_factor as lu_factor, lu_solve as lu_solve
from scipy.optimize._numdiff import group_columns as group_columns
from scipy.sparse import csc_matrix as csc_matrix, eye as eye, issparse as issparse
from scipy.sparse.linalg import splu as splu

MAX_ORDER: int
NEWTON_MAXITER: int
MIN_FACTOR: float
MAX_FACTOR: int

def compute_R(order, factor): ...
def change_D(D, order, factor) -> None: ...
def solve_bdf_system(fun, t_new, y_predict, c, psi, LU, solve_lu, scale, tol): ...

class BDF(OdeSolver):
    max_step: Incomplete
    h_abs: Incomplete
    h_abs_old: Incomplete
    error_norm_old: Incomplete
    newton_tol: Incomplete
    jac_factor: Incomplete
    lu: Incomplete
    solve_lu: Incomplete
    I: Incomplete
    gamma: Incomplete
    alpha: Incomplete
    error_const: Incomplete
    D: Incomplete
    order: int
    n_equal_steps: int
    LU: Incomplete
    def __init__(self, fun, t0, y0, t_bound, max_step=..., rtol: float = ..., atol: float = ..., jac: Incomplete | None = ..., jac_sparsity: Incomplete | None = ..., vectorized: bool = ..., first_step: Incomplete | None = ..., **extraneous) -> None: ...

class BdfDenseOutput(DenseOutput):
    order: Incomplete
    t_shift: Incomplete
    denom: Incomplete
    D: Incomplete
    def __init__(self, t_old, t, h, order, D) -> None: ...
