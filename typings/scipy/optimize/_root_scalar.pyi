from _typeshed import Incomplete

class MemoizeDer:
    fun: Incomplete
    vals: Incomplete
    x: Incomplete
    n_calls: int
    def __init__(self, fun) -> None: ...
    def __call__(self, x, *args): ...
    def fprime(self, x, *args): ...
    def fprime2(self, x, *args): ...
    def ncalls(self): ...

def root_scalar(f, args=..., method: Incomplete | None = ..., bracket: Incomplete | None = ..., fprime: Incomplete | None = ..., fprime2: Incomplete | None = ..., x0: Incomplete | None = ..., x1: Incomplete | None = ..., xtol: Incomplete | None = ..., rtol: Incomplete | None = ..., maxiter: Incomplete | None = ..., options: Incomplete | None = ...): ...
