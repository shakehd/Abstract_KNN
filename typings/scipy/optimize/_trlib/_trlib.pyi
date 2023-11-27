import scipy.optimize._trustregion
from scipy.optimize._trustregion import BaseQuadraticSubproblem as BaseQuadraticSubproblem

__test__: dict

class TRLIBQuadraticSubproblem(scipy.optimize._trustregion.BaseQuadraticSubproblem):
    def __init__(self, *args, **kwargs) -> None: ...
    def solve(self, *args, **kwargs): ...
