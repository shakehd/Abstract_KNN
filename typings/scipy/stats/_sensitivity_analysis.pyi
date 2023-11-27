import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from scipy._lib._util import DecimalNumber, IntNumber, SeedType
from scipy.stats._resampling import BootstrapResult
from typing import Callable, Literal, Protocol

@dataclass
class BootstrapSobolResult:
    first_order: BootstrapResult
    total_order: BootstrapResult
    def __init__(self, first_order, total_order) -> None: ...

@dataclass
class SobolResult:
    first_order: np.ndarray
    total_order: np.ndarray
    def bootstrap(self, confidence_level: DecimalNumber = ..., n_resamples: IntNumber = ...) -> BootstrapSobolResult: ...
    def __init__(self, first_order, total_order, _indices_method, _f_A, _f_B, _f_AB, _A, _B, _AB, _bootstrap_result) -> None: ...

class PPFDist(Protocol):
    @property
    def ppf(self) -> Callable[..., float]: ...

def sobol_indices(*, func: Callable[[np.ndarray], npt.ArrayLike] | dict[Literal['f_A', 'f_B', 'f_AB'], np.ndarray], n: IntNumber, dists: list[PPFDist] | None = ..., method: Callable | Literal['saltelli_2010'] = ..., random_state: SeedType = ...) -> SobolResult: ...
