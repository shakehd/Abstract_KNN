from _typeshed import Incomplete

def check_arguments(fun, y0, support_complex): ...

class OdeSolver:
    TOO_SMALL_STEP: str
    t_old: Incomplete
    t: Incomplete
    t_bound: Incomplete
    vectorized: Incomplete
    fun: Incomplete
    fun_single: Incomplete
    fun_vectorized: Incomplete
    direction: Incomplete
    n: Incomplete
    status: str
    nfev: int
    njev: int
    nlu: int
    def __init__(self, fun, t0, y0, t_bound, vectorized, support_complex: bool = ...) -> None: ...
    @property
    def step_size(self): ...
    def step(self): ...
    def dense_output(self): ...

class DenseOutput:
    t_old: Incomplete
    t: Incomplete
    t_min: Incomplete
    t_max: Incomplete
    def __init__(self, t_old, t) -> None: ...
    def __call__(self, t): ...

class ConstantDenseOutput(DenseOutput):
    value: Incomplete
    def __init__(self, t_old, t, value) -> None: ...
