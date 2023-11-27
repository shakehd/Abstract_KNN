from .base import DenseOutput as DenseOutput, OdeSolver as OdeSolver
from .common import validate_first_step as validate_first_step, validate_tol as validate_tol, warn_extraneous as warn_extraneous
from _typeshed import Incomplete
from scipy.integrate import ode as ode

class LSODA(OdeSolver):
    def __init__(self, fun, t0, y0, t_bound, first_step: Incomplete | None = ..., min_step: float = ..., max_step=..., rtol: float = ..., atol: float = ..., jac: Incomplete | None = ..., lband: Incomplete | None = ..., uband: Incomplete | None = ..., vectorized: bool = ..., **extraneous) -> None: ...

class LsodaDenseOutput(DenseOutput):
    h: Incomplete
    yh: Incomplete
    p: Incomplete
    def __init__(self, t_old, t, h, order, yh) -> None: ...
