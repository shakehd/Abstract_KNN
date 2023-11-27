from ._optimize import OptimizeWarning as OptimizeWarning
from _typeshed import Incomplete
from typing import NamedTuple

class _LPProblem(NamedTuple):
    c: Incomplete
    A_ub: Incomplete
    b_ub: Incomplete
    A_eq: Incomplete
    b_eq: Incomplete
    bounds: Incomplete
    x0: Incomplete
    integrality: Incomplete
