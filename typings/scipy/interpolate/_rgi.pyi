from _typeshed import Incomplete

class RegularGridInterpolator:
    method: Incomplete
    bounds_error: Incomplete
    values: Incomplete
    fill_value: Incomplete
    def __init__(self, points, values, method: str = ..., bounds_error: bool = ..., fill_value=...) -> None: ...
    def __call__(self, xi, method: Incomplete | None = ...): ...

def interpn(points, values, xi, method: str = ..., bounds_error: bool = ..., fill_value=...): ...
