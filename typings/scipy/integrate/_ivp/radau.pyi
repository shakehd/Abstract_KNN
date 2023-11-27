from .base import DenseOutput as DenseOutput, OdeSolver as OdeSolver
from .common import EPS as EPS, norm as norm, num_jac as num_jac, select_initial_step as select_initial_step, validate_first_step as validate_first_step, validate_max_step as validate_max_step, validate_tol as validate_tol, warn_extraneous as warn_extraneous
from _typeshed import Incomplete
from scipy.linalg import lu_factor as lu_factor, lu_solve as lu_solve
from scipy.optimize._numdiff import group_columns as group_columns
from scipy.sparse import csc_matrix as csc_matrix, eye as eye, issparse as issparse
from scipy.sparse.linalg import splu as splu

S6: Incomplete
C: Incomplete
E: Incomplete
MU_REAL: Incomplete
MU_COMPLEX: Incomplete
T: Incomplete
TI: Incomplete
TI_REAL: Incomplete
TI_COMPLEX: Incomplete
P: Incomplete
NEWTON_MAXITER: int
MIN_FACTOR: float
MAX_FACTOR: int

def solve_collocation_system(fun, t, y, h, Z0, scale, tol, LU_real, LU_complex, solve_lu): ...
def predict_factor(h_abs, h_abs_old, error_norm, error_norm_old): ...

class Radau(OdeSolver):
    y_old: Incomplete
    max_step: Incomplete
    f: Incomplete
    h_abs: Incomplete
    h_abs_old: Incomplete
    error_norm_old: Incomplete
    newton_tol: Incomplete
    sol: Incomplete
    jac_factor: Incomplete
    lu: Incomplete
    solve_lu: Incomplete
    I: Incomplete
    current_jac: bool
    LU_real: Incomplete
    LU_complex: Incomplete
    Z: Incomplete
    def __init__(self, fun, t0, y0, t_bound, max_step=..., rtol: float = ..., atol: float = ..., jac: Incomplete | None = ..., jac_sparsity: Incomplete | None = ..., vectorized: bool = ..., first_step: Incomplete | None = ..., **extraneous) -> None: ...

class RadauDenseOutput(DenseOutput):
    h: Incomplete
    Q: Incomplete
    order: Incomplete
    y_old: Incomplete
    def __init__(self, t_old, t, y_old, Q) -> None: ...
