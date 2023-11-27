import numpy as np
from _typeshed import Incomplete
from dataclasses import dataclass
from typing import NamedTuple

class Epps_Singleton_2sampResult(NamedTuple):
    statistic: Incomplete
    pvalue: Incomplete

def epps_singleton_2samp(x, y, t=...): ...
def poisson_means_test(k1, n1, k2, n2, *, diff: int = ..., alternative: str = ...): ...

class CramerVonMisesResult:
    statistic: Incomplete
    pvalue: Incomplete
    def __init__(self, statistic, pvalue) -> None: ...

def cramervonmises(rvs, cdf, args=...): ...

@dataclass
class SomersDResult:
    statistic: float
    pvalue: float
    table: np.ndarray
    def __init__(self, statistic, pvalue, table) -> None: ...

def somersd(x, y: Incomplete | None = ..., alternative: str = ...): ...

@dataclass
class BarnardExactResult:
    statistic: float
    pvalue: float
    def __init__(self, statistic, pvalue) -> None: ...

def barnard_exact(table, alternative: str = ..., pooled: bool = ..., n: int = ...): ...

@dataclass
class BoschlooExactResult:
    statistic: float
    pvalue: float
    def __init__(self, statistic, pvalue) -> None: ...

def boschloo_exact(table, alternative: str = ..., n: int = ...): ...
def cramervonmises_2samp(x, y, method: str = ...): ...

class TukeyHSDResult:
    statistic: Incomplete
    pvalue: Incomplete
    def __init__(self, statistic, pvalue, _nobs, _ntreatments, _stand_err) -> None: ...
    def confidence_interval(self, confidence_level: float = ...): ...

def tukey_hsd(*args): ...
