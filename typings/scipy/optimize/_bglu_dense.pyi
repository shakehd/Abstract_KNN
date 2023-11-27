from _typeshed import Incomplete
from scipy.linalg._basic import solve as solve, solve_triangular as solve_triangular
from scipy.linalg._decomp_lu import lu_factor as lu_factor, lu_solve as lu_solve

__test__: dict

class BGLU(LU):
    L: Incomplete
    U: Incomplete
    average_solve_times: Incomplete
    bglu_time: Incomplete
    mast: Incomplete
    max_updates: Incomplete
    ops_list: Incomplete
    pi: Incomplete
    pit: Incomplete
    plu: Incomplete
    solves: Incomplete
    updates: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def perform_perm(self, *args, **kwargs): ...
    def refactor(self, *args, **kwargs): ...
    def solve(self, *args, **kwargs): ...
    def update(self, *args, **kwargs): ...
    def update_basis(self, *args, **kwargs): ...
    def __reduce__(self): ...

class LU:
    A: Incomplete
    B: Incomplete
    b: Incomplete
    m: Incomplete
    n: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def solve(self, *args, **kwargs): ...
    def update(self, *args, **kwargs): ...
    def __reduce__(self): ...
