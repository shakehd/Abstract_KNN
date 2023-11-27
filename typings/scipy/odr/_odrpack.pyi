from _typeshed import Incomplete

odr: Incomplete

class OdrWarning(UserWarning): ...
class OdrError(Exception): ...
class OdrStop(Exception): ...
odr_error = OdrError
odr_stop = OdrStop

class Data:
    x: Incomplete
    y: Incomplete
    we: Incomplete
    wd: Incomplete
    fix: Incomplete
    meta: Incomplete
    def __init__(self, x, y: Incomplete | None = ..., we: Incomplete | None = ..., wd: Incomplete | None = ..., fix: Incomplete | None = ..., meta: Incomplete | None = ...) -> None: ...
    def set_meta(self, **kwds) -> None: ...
    def __getattr__(self, attr): ...

class RealData(Data):
    x: Incomplete
    y: Incomplete
    sx: Incomplete
    sy: Incomplete
    covx: Incomplete
    covy: Incomplete
    fix: Incomplete
    meta: Incomplete
    def __init__(self, x, y: Incomplete | None = ..., sx: Incomplete | None = ..., sy: Incomplete | None = ..., covx: Incomplete | None = ..., covy: Incomplete | None = ..., fix: Incomplete | None = ..., meta: Incomplete | None = ...) -> None: ...
    def __getattr__(self, attr): ...

class Model:
    fcn: Incomplete
    fjacb: Incomplete
    fjacd: Incomplete
    extra_args: Incomplete
    estimate: Incomplete
    implicit: Incomplete
    meta: Incomplete
    def __init__(self, fcn, fjacb: Incomplete | None = ..., fjacd: Incomplete | None = ..., extra_args: Incomplete | None = ..., estimate: Incomplete | None = ..., implicit: int = ..., meta: Incomplete | None = ...) -> None: ...
    def set_meta(self, **kwds) -> None: ...
    def __getattr__(self, attr): ...

class Output:
    beta: Incomplete
    sd_beta: Incomplete
    cov_beta: Incomplete
    stopreason: Incomplete
    def __init__(self, output) -> None: ...
    def pprint(self) -> None: ...

class ODR:
    data: Incomplete
    model: Incomplete
    beta0: Incomplete
    delta0: Incomplete
    ifixx: Incomplete
    ifixb: Incomplete
    job: Incomplete
    iprint: Incomplete
    errfile: Incomplete
    rptfile: Incomplete
    ndigit: Incomplete
    taufac: Incomplete
    sstol: Incomplete
    partol: Incomplete
    maxit: Incomplete
    stpb: Incomplete
    stpd: Incomplete
    sclb: Incomplete
    scld: Incomplete
    work: Incomplete
    iwork: Incomplete
    output: Incomplete
    def __init__(self, data, model, beta0: Incomplete | None = ..., delta0: Incomplete | None = ..., ifixb: Incomplete | None = ..., ifixx: Incomplete | None = ..., job: Incomplete | None = ..., iprint: Incomplete | None = ..., errfile: Incomplete | None = ..., rptfile: Incomplete | None = ..., ndigit: Incomplete | None = ..., taufac: Incomplete | None = ..., sstol: Incomplete | None = ..., partol: Incomplete | None = ..., maxit: Incomplete | None = ..., stpb: Incomplete | None = ..., stpd: Incomplete | None = ..., sclb: Incomplete | None = ..., scld: Incomplete | None = ..., work: Incomplete | None = ..., iwork: Incomplete | None = ..., overwrite: bool = ...) -> None: ...
    def set_job(self, fit_type: Incomplete | None = ..., deriv: Incomplete | None = ..., var_calc: Incomplete | None = ..., del_init: Incomplete | None = ..., restart: Incomplete | None = ...) -> None: ...
    def set_iprint(self, init: Incomplete | None = ..., so_init: Incomplete | None = ..., iter: Incomplete | None = ..., so_iter: Incomplete | None = ..., iter_step: Incomplete | None = ..., final: Incomplete | None = ..., so_final: Incomplete | None = ...) -> None: ...
    def run(self): ...
    def restart(self, iter: Incomplete | None = ...): ...
