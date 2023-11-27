import numpy.typing as npt
from ._constraints import Bounds
from scipy.optimize import OptimizeResult
from typing import Any, Callable, Iterable

def direct(func: Callable[[npt.ArrayLike, tuple[Any]], float], bounds: Iterable | Bounds, *, args: tuple = ..., eps: float = ..., maxfun: int | None = ..., maxiter: int = ..., locally_biased: bool = ..., f_min: float = ..., f_min_rtol: float = ..., vol_tol: float = ..., len_tol: float = ..., callback: Callable[[npt.ArrayLike], None] | None = ...) -> OptimizeResult: ...
