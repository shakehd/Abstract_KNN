from ._trustregion import BaseQuadraticSubproblem
from _typeshed import Incomplete

def estimate_smallest_singular_value(U): ...
def singular_leading_submatrix(A, U, k): ...

class IterativeSubproblem(BaseQuadraticSubproblem):
    UPDATE_COEFF: float
    EPS: Incomplete
    previous_tr_radius: int
    lambda_lb: Incomplete
    niter: int
    k_easy: Incomplete
    k_hard: Incomplete
    dimension: Incomplete
    hess_inf: Incomplete
    hess_fro: Incomplete
    CLOSE_TO_ZERO: Incomplete
    def __init__(self, x, fun, jac, hess, hessp: Incomplete | None = ..., k_easy: float = ..., k_hard: float = ...) -> None: ...
    lambda_current: Incomplete
    def solve(self, tr_radius): ...

# Names in __all__ with no definition:
#   _minimize_trustregion_exact
