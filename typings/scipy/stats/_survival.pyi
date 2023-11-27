import numpy as np
import numpy.typing as npt
from _typeshed import Incomplete
from dataclasses import dataclass
from scipy.stats._censored_data import CensoredData
from typing import Literal

@dataclass
class EmpiricalDistributionFunction:
    quantiles: np.ndarray
    probabilities: np.ndarray
    def __init__(self, q, p, n, d, kind) -> None: ...
    def evaluate(self, x): ...
    def plot(self, ax: Incomplete | None = ..., **matplotlib_kwargs): ...
    def confidence_interval(self, confidence_level: float = ..., *, method: str = ...): ...

@dataclass
class ECDFResult:
    cdf: EmpiricalDistributionFunction
    sf: EmpiricalDistributionFunction
    def __init__(self, q, cdf, sf, n, d) -> None: ...

def ecdf(sample: npt.ArrayLike | CensoredData) -> ECDFResult: ...

@dataclass
class LogRankResult:
    statistic: np.ndarray
    pvalue: np.ndarray
    def __init__(self, statistic, pvalue) -> None: ...

def logrank(x: npt.ArrayLike | CensoredData, y: npt.ArrayLike | CensoredData, alternative: Literal['two-sided', 'less', 'greater'] = ...) -> LogRankResult: ...
