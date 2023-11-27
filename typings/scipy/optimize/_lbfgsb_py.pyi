from _typeshed import Incomplete
from scipy.sparse.linalg import LinearOperator

def fmin_l_bfgs_b(func, x0, fprime: Incomplete | None = ..., args=..., approx_grad: int = ..., bounds: Incomplete | None = ..., m: int = ..., factr: float = ..., pgtol: float = ..., epsilon: float = ..., iprint: int = ..., maxfun: int = ..., maxiter: int = ..., disp: Incomplete | None = ..., callback: Incomplete | None = ..., maxls: int = ...): ...

class LbfgsInvHessProduct(LinearOperator):
    sk: Incomplete
    yk: Incomplete
    n_corrs: Incomplete
    rho: Incomplete
    def __init__(self, sk, yk) -> None: ...
    def todense(self): ...
