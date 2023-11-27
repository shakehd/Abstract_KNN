import numpy as np
from . import dop853_coefficients as dop853_coefficients
from .base import DenseOutput as DenseOutput, OdeSolver as OdeSolver
from .common import norm as norm, select_initial_step as select_initial_step, validate_first_step as validate_first_step, validate_max_step as validate_max_step, validate_tol as validate_tol, warn_extraneous as warn_extraneous
from _typeshed import Incomplete

SAFETY: float
MIN_FACTOR: float
MAX_FACTOR: int

def rk_step(fun, t, y, f, h, A, B, C, K): ...

class RungeKutta(OdeSolver):
    C: np.ndarray
    A: np.ndarray
    B: np.ndarray
    E: np.ndarray
    P: np.ndarray
    order: int
    error_estimator_order: int
    n_stages: int
    y_old: Incomplete
    max_step: Incomplete
    f: Incomplete
    h_abs: Incomplete
    K: Incomplete
    error_exponent: Incomplete
    h_previous: Incomplete
    def __init__(self, fun, t0, y0, t_bound, max_step=..., rtol: float = ..., atol: float = ..., vectorized: bool = ..., first_step: Incomplete | None = ..., **extraneous) -> None: ...

class RK23(RungeKutta):
    order: int
    error_estimator_order: int
    n_stages: int
    C: Incomplete
    A: Incomplete
    B: Incomplete
    E: Incomplete
    P: Incomplete

class RK45(RungeKutta):
    order: int
    error_estimator_order: int
    n_stages: int
    C: Incomplete
    A: Incomplete
    B: Incomplete
    E: Incomplete
    P: Incomplete

class DOP853(RungeKutta):
    n_stages: Incomplete
    order: int
    error_estimator_order: int
    A: Incomplete
    B: Incomplete
    C: Incomplete
    E3: Incomplete
    E5: Incomplete
    D: Incomplete
    A_EXTRA: Incomplete
    C_EXTRA: Incomplete
    K_extended: Incomplete
    K: Incomplete
    def __init__(self, fun, t0, y0, t_bound, max_step=..., rtol: float = ..., atol: float = ..., vectorized: bool = ..., first_step: Incomplete | None = ..., **extraneous) -> None: ...

class RkDenseOutput(DenseOutput):
    h: Incomplete
    Q: Incomplete
    order: Incomplete
    y_old: Incomplete
    def __init__(self, t_old, t, y_old, Q) -> None: ...

class Dop853DenseOutput(DenseOutput):
    h: Incomplete
    F: Incomplete
    y_old: Incomplete
    def __init__(self, t_old, t, y_old, F) -> None: ...
