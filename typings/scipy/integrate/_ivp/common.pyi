from _typeshed import Incomplete
from scipy.sparse import coo_matrix as coo_matrix, find as find

EPS: Incomplete

def validate_first_step(first_step, t0, t_bound): ...
def validate_max_step(max_step): ...
def warn_extraneous(extraneous) -> None: ...
def validate_tol(rtol, atol, n): ...
def norm(x): ...
def select_initial_step(fun, t0, y0, f0, direction, order, rtol, atol): ...

class OdeSolution:
    n_segments: Incomplete
    ts: Incomplete
    interpolants: Incomplete
    t_min: Incomplete
    t_max: Incomplete
    ascending: bool
    ts_sorted: Incomplete
    def __init__(self, ts, interpolants) -> None: ...
    def __call__(self, t): ...

NUM_JAC_DIFF_REJECT: Incomplete
NUM_JAC_DIFF_SMALL: Incomplete
NUM_JAC_DIFF_BIG: Incomplete
NUM_JAC_MIN_FACTOR: Incomplete
NUM_JAC_FACTOR_INCREASE: int
NUM_JAC_FACTOR_DECREASE: float

def num_jac(fun, t, y, f, threshold, factor, sparsity: Incomplete | None = ...): ...
