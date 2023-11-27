from typing import Any

physical_constants: dict[str, tuple[float, str, float]]

class ConstantWarning(DeprecationWarning): ...

def value(key: str) -> float: ...
def unit(key: str) -> str: ...
def precision(key: str) -> float: ...
def find(sub: str | None = ..., disp: bool = ...) -> Any: ...
