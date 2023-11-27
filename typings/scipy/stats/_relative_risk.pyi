from ._common import ConfidenceInterval as ConfidenceInterval
from dataclasses import dataclass
from scipy.special import ndtri as ndtri

@dataclass
class RelativeRiskResult:
    relative_risk: float
    exposed_cases: int
    exposed_total: int
    control_cases: int
    control_total: int
    def confidence_interval(self, confidence_level: float = ...): ...
    def __init__(self, relative_risk, exposed_cases, exposed_total, control_cases, control_total) -> None: ...

def relative_risk(exposed_cases, exposed_total, control_cases, control_total): ...
