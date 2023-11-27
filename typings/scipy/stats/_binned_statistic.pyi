from _typeshed import Incomplete
from typing import NamedTuple

class BinnedStatisticResult(NamedTuple):
    statistic: Incomplete
    bin_edges: Incomplete
    binnumber: Incomplete

def binned_statistic(x, values, statistic: str = ..., bins: int = ..., range: Incomplete | None = ...): ...

class BinnedStatistic2dResult(NamedTuple):
    statistic: Incomplete
    x_edge: Incomplete
    y_edge: Incomplete
    binnumber: Incomplete

def binned_statistic_2d(x, y, values, statistic: str = ..., bins: int = ..., range: Incomplete | None = ..., expand_binnumbers: bool = ...): ...

class BinnedStatisticddResult(NamedTuple):
    statistic: Incomplete
    bin_edges: Incomplete
    binnumber: Incomplete

def binned_statistic_dd(sample, values, statistic: str = ..., bins: int = ..., range: Incomplete | None = ..., expand_binnumbers: bool = ..., binned_statistic_result: Incomplete | None = ...): ...
