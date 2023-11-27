from _typeshed import Incomplete

class FPUModeChangeWarning(RuntimeWarning): ...

class PytestTester:
    module_name: Incomplete
    def __init__(self, module_name) -> None: ...
    def __call__(self, label: str = ..., verbose: int = ..., extra_argv: Incomplete | None = ..., doctests: bool = ..., coverage: bool = ..., tests: Incomplete | None = ..., parallel: Incomplete | None = ...): ...

class _TestPythranFunc:
    ALL_INTEGER: Incomplete
    ALL_FLOAT: Incomplete
    ALL_COMPLEX: Incomplete
    arguments: Incomplete
    partialfunc: Incomplete
    expected: Incomplete
    def setup_method(self) -> None: ...
    def get_optional_args(self, func): ...
    def get_max_dtype_list_length(self): ...
    def get_dtype(self, dtype_list, dtype_idx): ...
    def test_all_dtypes(self) -> None: ...
    def test_views(self) -> None: ...
    def test_strided(self) -> None: ...

def check_free_memory(free_mb) -> None: ...
