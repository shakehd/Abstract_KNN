import numpy as np
from _typeshed import Incomplete
from scipy.linalg import solve_triangular as solve_triangular, svdvals as svdvals
from scipy.linalg._decomp_schur import rsf2csf as rsf2csf, schur as schur
from scipy.linalg._matfuncs import funm as funm
from scipy.linalg._matfuncs_sqrtm import SqrtmError as SqrtmError
from scipy.sparse.linalg import onenormest as onenormest
from scipy.sparse.linalg._interface import LinearOperator as LinearOperator

class LogmRankWarning(UserWarning): ...
class LogmExactlySingularWarning(LogmRankWarning): ...
class LogmNearlySingularWarning(LogmRankWarning): ...
class LogmError(np.linalg.LinAlgError): ...
class FractionalMatrixPowerError(np.linalg.LinAlgError): ...

class _MatrixM1PowerOperator(LinearOperator):
    ndim: Incomplete
    shape: Incomplete
    def __init__(self, A, p) -> None: ...
