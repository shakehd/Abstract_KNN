from ._constraints import Bounds as Bounds, LinearConstraint as LinearConstraint
from ._optimize import OptimizeResult as OptimizeResult
from _typeshed import Incomplete
from scipy.sparse import csc_array as csc_array, issparse as issparse, vstack as vstack

def milp(c, *, integrality: Incomplete | None = ..., bounds: Incomplete | None = ..., constraints: Incomplete | None = ..., options: Incomplete | None = ...): ...
