from ._differentiable_functions import IdentityVectorFunction as IdentityVectorFunction, LinearVectorFunction as LinearVectorFunction, VectorFunction as VectorFunction
from ._hessian_update_strategy import BFGS as BFGS
from ._optimize import OptimizeWarning as OptimizeWarning
from _typeshed import Incomplete
from scipy.sparse import issparse as issparse

class NonlinearConstraint:
    fun: Incomplete
    lb: Incomplete
    ub: Incomplete
    finite_diff_rel_step: Incomplete
    finite_diff_jac_sparsity: Incomplete
    jac: Incomplete
    hess: Incomplete
    keep_feasible: Incomplete
    def __init__(self, fun, lb, ub, jac: str = ..., hess=..., keep_feasible: bool = ..., finite_diff_rel_step: Incomplete | None = ..., finite_diff_jac_sparsity: Incomplete | None = ...) -> None: ...

class LinearConstraint:
    A: Incomplete
    lb: Incomplete
    ub: Incomplete
    keep_feasible: Incomplete
    def __init__(self, A, lb=..., ub=..., keep_feasible: bool = ...) -> None: ...
    def residual(self, x): ...

class Bounds:
    lb: Incomplete
    ub: Incomplete
    keep_feasible: Incomplete
    def __init__(self, lb=..., ub=..., keep_feasible: bool = ...) -> None: ...
    def residual(self, x): ...

class PreparedConstraint:
    fun: Incomplete
    bounds: Incomplete
    keep_feasible: Incomplete
    def __init__(self, constraint, x0, sparse_jacobian: Incomplete | None = ..., finite_diff_bounds=...) -> None: ...
    def violation(self, x): ...

def new_bounds_to_old(lb, ub, n): ...
def old_bound_to_new(bounds): ...
def strict_bounds(lb, ub, keep_feasible, n_vars): ...
def new_constraint_to_old(con, x0): ...
def old_constraint_to_new(ic, con): ...
