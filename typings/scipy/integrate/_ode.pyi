from _typeshed import Incomplete

class ode:
    stiff: int
    f: Incomplete
    jac: Incomplete
    f_params: Incomplete
    jac_params: Incomplete
    def __init__(self, f, jac: Incomplete | None = ...) -> None: ...
    @property
    def y(self): ...
    t: Incomplete
    def set_initial_value(self, y, t: float = ...): ...
    def set_integrator(self, name, **integrator_params): ...
    def integrate(self, t, step: bool = ..., relax: bool = ...): ...
    def successful(self): ...
    def get_return_code(self): ...
    def set_f_params(self, *args): ...
    def set_jac_params(self, *args): ...
    def set_solout(self, solout) -> None: ...

class complex_ode(ode):
    cf: Incomplete
    cjac: Incomplete
    def __init__(self, f, jac: Incomplete | None = ...) -> None: ...
    @property
    def y(self): ...
    def set_integrator(self, name, **integrator_params): ...
    tmp: Incomplete
    def set_initial_value(self, y, t: float = ...): ...
    def integrate(self, t, step: bool = ..., relax: bool = ...): ...
    def set_solout(self, solout) -> None: ...

class IntegratorConcurrencyError(RuntimeError):
    def __init__(self, name) -> None: ...

class IntegratorBase:
    runner: Incomplete
    success: Incomplete
    istate: Incomplete
    supports_run_relax: Incomplete
    supports_step: Incomplete
    supports_solout: bool
    integrator_classes: Incomplete
    scalar = float
    handle: Incomplete
    def acquire_new_handle(self) -> None: ...
    def check_handle(self) -> None: ...
    def reset(self, n, has_jac) -> None: ...
    def run(self, f, jac, y0, t0, t1, f_params, jac_params) -> None: ...
    def step(self, f, jac, y0, t0, t1, f_params, jac_params) -> None: ...
    def run_relax(self, f, jac, y0, t0, t1, f_params, jac_params) -> None: ...

class vode(IntegratorBase):
    runner: Incomplete
    messages: Incomplete
    supports_run_relax: int
    supports_step: int
    active_global_handle: int
    meth: int
    with_jacobian: Incomplete
    rtol: Incomplete
    atol: Incomplete
    mu: Incomplete
    ml: Incomplete
    order: Incomplete
    nsteps: Incomplete
    max_step: Incomplete
    min_step: Incomplete
    first_step: Incomplete
    success: int
    initialized: bool
    def __init__(self, method: str = ..., with_jacobian: bool = ..., rtol: float = ..., atol: float = ..., lband: Incomplete | None = ..., uband: Incomplete | None = ..., order: int = ..., nsteps: int = ..., max_step: float = ..., min_step: float = ..., first_step: float = ...) -> None: ...
    rwork: Incomplete
    iwork: Incomplete
    call_args: Incomplete
    def reset(self, n, has_jac) -> None: ...
    istate: Incomplete
    def run(self, f, jac, y0, t0, t1, f_params, jac_params): ...
    def step(self, *args): ...
    def run_relax(self, *args): ...

class zvode(vode):
    runner: Incomplete
    supports_run_relax: int
    supports_step: int
    scalar = complex
    active_global_handle: int
    zwork: Incomplete
    rwork: Incomplete
    iwork: Incomplete
    call_args: Incomplete
    success: int
    initialized: bool
    def reset(self, n, has_jac) -> None: ...

class dopri5(IntegratorBase):
    runner: Incomplete
    name: str
    supports_solout: bool
    messages: Incomplete
    rtol: Incomplete
    atol: Incomplete
    nsteps: Incomplete
    max_step: Incomplete
    first_step: Incomplete
    safety: Incomplete
    ifactor: Incomplete
    dfactor: Incomplete
    beta: Incomplete
    verbosity: Incomplete
    success: int
    def __init__(self, rtol: float = ..., atol: float = ..., nsteps: int = ..., max_step: float = ..., first_step: float = ..., safety: float = ..., ifactor: float = ..., dfactor: float = ..., beta: float = ..., method: Incomplete | None = ..., verbosity: int = ...) -> None: ...
    solout: Incomplete
    solout_cmplx: Incomplete
    iout: int
    def set_solout(self, solout, complex: bool = ...) -> None: ...
    work: Incomplete
    iwork: Incomplete
    call_args: Incomplete
    def reset(self, n, has_jac) -> None: ...
    istate: Incomplete
    def run(self, f, jac, y0, t0, t1, f_params, jac_params): ...

class dop853(dopri5):
    runner: Incomplete
    name: str
    def __init__(self, rtol: float = ..., atol: float = ..., nsteps: int = ..., max_step: float = ..., first_step: float = ..., safety: float = ..., ifactor: float = ..., dfactor: float = ..., beta: float = ..., method: Incomplete | None = ..., verbosity: int = ...) -> None: ...
    work: Incomplete
    iwork: Incomplete
    call_args: Incomplete
    success: int
    def reset(self, n, has_jac) -> None: ...

class lsoda(IntegratorBase):
    runner: Incomplete
    active_global_handle: int
    messages: Incomplete
    with_jacobian: Incomplete
    rtol: Incomplete
    atol: Incomplete
    mu: Incomplete
    ml: Incomplete
    max_order_ns: Incomplete
    max_order_s: Incomplete
    nsteps: Incomplete
    max_step: Incomplete
    min_step: Incomplete
    first_step: Incomplete
    ixpr: Incomplete
    max_hnil: Incomplete
    success: int
    initialized: bool
    def __init__(self, with_jacobian: bool = ..., rtol: float = ..., atol: float = ..., lband: Incomplete | None = ..., uband: Incomplete | None = ..., nsteps: int = ..., max_step: float = ..., min_step: float = ..., first_step: float = ..., ixpr: int = ..., max_hnil: int = ..., max_order_ns: int = ..., max_order_s: int = ..., method: Incomplete | None = ...) -> None: ...
    rwork: Incomplete
    iwork: Incomplete
    call_args: Incomplete
    def reset(self, n, has_jac) -> None: ...
    istate: Incomplete
    def run(self, f, jac, y0, t0, t1, f_params, jac_params): ...
    def step(self, *args): ...
    def run_relax(self, *args): ...
