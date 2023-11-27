from ._rotation import Rotation as Rotation
from _typeshed import Incomplete
from scipy.linalg import solve_banded as solve_banded

class RotationSpline:
    MAX_ITER: int
    TOL: float
    times: Incomplete
    rotations: Incomplete
    interpolator: Incomplete
    def __init__(self, times, rotations) -> None: ...
    def __call__(self, times, order: int = ...): ...
