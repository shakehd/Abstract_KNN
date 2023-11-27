from .._constraints import Bounds as Bounds, LinearConstraint as LinearConstraint, NonlinearConstraint as NonlinearConstraint, PreparedConstraint as PreparedConstraint, strict_bounds as strict_bounds
from .._differentiable_functions import ScalarFunction as ScalarFunction, VectorFunction as VectorFunction
from .._hessian_update_strategy import BFGS as BFGS
from .._optimize import OptimizeResult as OptimizeResult
from .canonical_constraint import CanonicalConstraint as CanonicalConstraint, initial_constraints_as_canonical as initial_constraints_as_canonical
from .equality_constrained_sqp import equality_constrained_sqp as equality_constrained_sqp
from .report import BasicReport as BasicReport, IPReport as IPReport, SQPReport as SQPReport
from .tr_interior_point import tr_interior_point as tr_interior_point
from _typeshed import Incomplete
from scipy.sparse.linalg import LinearOperator as LinearOperator

TERMINATION_MESSAGES: Incomplete

class HessianLinearOperator:
    hessp: Incomplete
    n: Incomplete
    def __init__(self, hessp, n) -> None: ...
    def __call__(self, x, *args): ...

class LagrangianHessian:
    n: Incomplete
    objective_hess: Incomplete
    constraints_hess: Incomplete
    def __init__(self, n, objective_hess, constraints_hess) -> None: ...
    def __call__(self, x, v_eq=..., v_ineq=...): ...

def update_state_sqp(state, x, last_iteration_failed, objective, prepared_constraints, start_time, tr_radius, constr_penalty, cg_info): ...
def update_state_ip(state, x, last_iteration_failed, objective, prepared_constraints, start_time, tr_radius, constr_penalty, cg_info, barrier_parameter, barrier_tolerance): ...
