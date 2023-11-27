from _typeshed import Incomplete

class CanonicalConstraint:
    n_eq: Incomplete
    n_ineq: Incomplete
    fun: Incomplete
    jac: Incomplete
    hess: Incomplete
    keep_feasible: Incomplete
    def __init__(self, n_eq, n_ineq, fun, jac, hess, keep_feasible) -> None: ...
    @classmethod
    def from_PreparedConstraint(cls, constraint): ...
    @classmethod
    def empty(cls, n): ...
    @classmethod
    def concatenate(cls, canonical_constraints, sparse_jacobian): ...

def initial_constraints_as_canonical(n, prepared_constraints, sparse_jacobian): ...
