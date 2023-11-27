from .interpnd import CloughTocher2DInterpolator as CloughTocher2DInterpolator, LinearNDInterpolator as LinearNDInterpolator, NDInterpolatorBase
from _typeshed import Incomplete

class NearestNDInterpolator(NDInterpolatorBase):
    tree: Incomplete
    values: Incomplete
    def __init__(self, x, y, rescale: bool = ..., tree_options: Incomplete | None = ...) -> None: ...
    def __call__(self, *args): ...

def griddata(points, values, xi, method: str = ..., fill_value=..., rescale: bool = ...): ...
