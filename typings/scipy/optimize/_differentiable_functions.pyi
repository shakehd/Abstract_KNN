from ._hessian_update_strategy import HessianUpdateStrategy as HessianUpdateStrategy
from ._numdiff import approx_derivative as approx_derivative, group_columns as group_columns
from _typeshed import Incomplete
from scipy.sparse.linalg import LinearOperator as LinearOperator

FD_METHODS: Incomplete

class ScalarFunction:
    x: Incomplete
    n: Incomplete
    nfev: int
    ngev: int
    nhev: int
    f_updated: bool
    g_updated: bool
    H_updated: bool
    f: Incomplete
    g: Incomplete
    H: Incomplete
    x_prev: Incomplete
    g_prev: Incomplete
    def __init__(self, fun, x0, args, grad, hess, finite_diff_rel_step, finite_diff_bounds, epsilon: Incomplete | None = ...) -> None: ...
    def fun(self, x): ...
    def grad(self, x): ...
    def hess(self, x): ...
    def fun_and_grad(self, x): ...

class VectorFunction:
    x: Incomplete
    n: Incomplete
    nfev: int
    njev: int
    nhev: int
    f_updated: bool
    J_updated: bool
    H_updated: bool
    x_diff: Incomplete
    f: Incomplete
    v: Incomplete
    m: Incomplete
    J: Incomplete
    sparse_jacobian: bool
    H: Incomplete
    x_prev: Incomplete
    J_prev: Incomplete
    def __init__(self, fun, x0, jac, hess, finite_diff_rel_step, finite_diff_jac_sparsity, finite_diff_bounds, sparse_jacobian) -> None: ...
    def fun(self, x): ...
    def jac(self, x): ...
    def hess(self, x, v): ...

class LinearVectorFunction:
    J: Incomplete
    sparse_jacobian: bool
    x: Incomplete
    f: Incomplete
    f_updated: bool
    v: Incomplete
    H: Incomplete
    def __init__(self, A, x0, sparse_jacobian) -> None: ...
    def fun(self, x): ...
    def jac(self, x): ...
    def hess(self, x, v): ...

class IdentityVectorFunction(LinearVectorFunction):
    def __init__(self, x0, sparse_jacobian) -> None: ...
