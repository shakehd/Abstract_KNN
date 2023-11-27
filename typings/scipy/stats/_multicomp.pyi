import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from scipy._lib._util import DecimalNumber, SeedType
from scipy.stats._common import ConfidenceInterval
from typing import Literal

@dataclass
class DunnettResult:
    statistic: np.ndarray
    pvalue: np.ndarray
    def confidence_interval(self, confidence_level: DecimalNumber = ...) -> ConfidenceInterval: ...
    def __init__(self, statistic, pvalue, _alternative, _rho, _df, _std, _mean_samples, _mean_control, _n_samples, _n_control, _rng, _ci, _ci_cl) -> None: ...

def dunnett(*samples: npt.ArrayLike, control: npt.ArrayLike, alternative: Literal['two-sided', 'less', 'greater'] = ..., random_state: SeedType = ...) -> DunnettResult: ...
