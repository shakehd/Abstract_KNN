from _typeshed import Incomplete

class MissingModule:
    name: Incomplete
    def __init__(self, name) -> None: ...

def with_special_errors(func): ...
def assert_func_equal(func, results, points, rtol: Incomplete | None = ..., atol: Incomplete | None = ..., param_filter: Incomplete | None = ..., knownfailure: Incomplete | None = ..., vectorized: bool = ..., dtype: Incomplete | None = ..., nan_ok: bool = ..., ignore_inf_sign: bool = ..., distinguish_nan_and_inf: bool = ...) -> None: ...

class FuncData:
    func: Incomplete
    data: Incomplete
    dataname: Incomplete
    param_columns: Incomplete
    result_columns: Incomplete
    result_func: Incomplete
    rtol: Incomplete
    atol: Incomplete
    param_filter: Incomplete
    knownfailure: Incomplete
    nan_ok: Incomplete
    vectorized: Incomplete
    ignore_inf_sign: Incomplete
    distinguish_nan_and_inf: Incomplete
    def __init__(self, func, data, param_columns, result_columns: Incomplete | None = ..., result_func: Incomplete | None = ..., rtol: Incomplete | None = ..., atol: Incomplete | None = ..., param_filter: Incomplete | None = ..., knownfailure: Incomplete | None = ..., dataname: Incomplete | None = ..., nan_ok: bool = ..., vectorized: bool = ..., ignore_inf_sign: bool = ..., distinguish_nan_and_inf: bool = ...) -> None: ...
    def get_tolerances(self, dtype): ...
    def check(self, data: Incomplete | None = ..., dtype: Incomplete | None = ..., dtypes: Incomplete | None = ...): ...
