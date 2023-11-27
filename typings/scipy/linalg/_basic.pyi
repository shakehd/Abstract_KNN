from _typeshed import Incomplete

def solve(a, b, lower: bool = ..., overwrite_a: bool = ..., overwrite_b: bool = ..., check_finite: bool = ..., assume_a: str = ..., transposed: bool = ...): ...
def solve_triangular(a, b, trans: int = ..., lower: bool = ..., unit_diagonal: bool = ..., overwrite_b: bool = ..., check_finite: bool = ...): ...
def solve_banded(l_and_u, ab, b, overwrite_ab: bool = ..., overwrite_b: bool = ..., check_finite: bool = ...): ...
def solveh_banded(ab, b, overwrite_ab: bool = ..., overwrite_b: bool = ..., lower: bool = ..., check_finite: bool = ...): ...
def solve_toeplitz(c_or_cr, b, check_finite: bool = ...): ...
def solve_circulant(c, b, singular: str = ..., tol: Incomplete | None = ..., caxis: int = ..., baxis: int = ..., outaxis: int = ...): ...
def inv(a, overwrite_a: bool = ..., check_finite: bool = ...): ...
def det(a, overwrite_a: bool = ..., check_finite: bool = ...): ...
def lstsq(a, b, cond: Incomplete | None = ..., overwrite_a: bool = ..., overwrite_b: bool = ..., check_finite: bool = ..., lapack_driver: Incomplete | None = ...): ...
def pinv(a, atol: Incomplete | None = ..., rtol: Incomplete | None = ..., return_rank: bool = ..., check_finite: bool = ..., cond: Incomplete | None = ..., rcond: Incomplete | None = ...): ...
def pinvh(a, atol: Incomplete | None = ..., rtol: Incomplete | None = ..., lower: bool = ..., return_rank: bool = ..., check_finite: bool = ...): ...
def matrix_balance(A, permute: bool = ..., scale: bool = ..., separate: bool = ..., overwrite_a: bool = ...): ...
def matmul_toeplitz(c_or_cr, x, check_finite: bool = ..., workers: Incomplete | None = ...): ...
