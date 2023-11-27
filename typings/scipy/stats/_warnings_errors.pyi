from _typeshed import Incomplete

class DegenerateDataWarning(RuntimeWarning):
    args: Incomplete
    def __init__(self, msg: Incomplete | None = ...) -> None: ...

class ConstantInputWarning(DegenerateDataWarning):
    args: Incomplete
    def __init__(self, msg: Incomplete | None = ...) -> None: ...

class NearConstantInputWarning(DegenerateDataWarning):
    args: Incomplete
    def __init__(self, msg: Incomplete | None = ...) -> None: ...

class FitError(RuntimeError):
    args: Incomplete
    def __init__(self, msg: Incomplete | None = ...) -> None: ...
