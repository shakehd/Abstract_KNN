from _typeshed import Incomplete
from scipy import optimize as optimize, stats as stats
from scipy._lib._util import check_random_state as check_random_state
from typing import NamedTuple

class FitResult:
    discrete: Incomplete
    pxf: Incomplete
    params: Incomplete
    success: Incomplete
    message: Incomplete
    def __init__(self, dist, data, discrete, res) -> None: ...
    def nllf(self, params: Incomplete | None = ..., data: Incomplete | None = ...): ...
    def plot(self, ax: Incomplete | None = ..., *, plot_type: str = ...): ...

def fit(dist, data, bounds: Incomplete | None = ..., *, guess: Incomplete | None = ..., method: str = ..., optimizer=...): ...

class GoodnessOfFitResult(NamedTuple):
    fit_result: Incomplete
    statistic: Incomplete
    pvalue: Incomplete
    null_distribution: Incomplete

def goodness_of_fit(dist, data, *, known_params: Incomplete | None = ..., fit_params: Incomplete | None = ..., guessed_params: Incomplete | None = ..., statistic: str = ..., n_mc_samples: int = ..., random_state: Incomplete | None = ...): ...
