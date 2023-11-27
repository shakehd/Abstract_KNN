import numpy as np
from _typeshed import Incomplete

miINT8: int
miUINT8: int
miINT16: int
miUINT16: int
miINT32: int
miUINT32: int
miSINGLE: int
miDOUBLE: int
miINT64: int
miUINT64: int
miMATRIX: int
miCOMPRESSED: int
miUTF8: int
miUTF16: int
miUTF32: int
mxCELL_CLASS: int
mxSTRUCT_CLASS: int
mxOBJECT_CLASS: int
mxCHAR_CLASS: int
mxSPARSE_CLASS: int
mxDOUBLE_CLASS: int
mxSINGLE_CLASS: int
mxINT8_CLASS: int
mxUINT8_CLASS: int
mxINT16_CLASS: int
mxUINT16_CLASS: int
mxINT32_CLASS: int
mxUINT32_CLASS: int
mxINT64_CLASS: int
mxUINT64_CLASS: int
mxFUNCTION_CLASS: int
mxOPAQUE_CLASS: int
mxOBJECT_CLASS_FROM_MATRIX_H: int
mdtypes_template: Incomplete
mclass_dtypes_template: Incomplete
mclass_info: Incomplete
NP_TO_MTYPES: Incomplete
NP_TO_MXTYPES: Incomplete
codecs_template: Incomplete
MDTYPES: Incomplete

class mat_struct: ...

class MatlabObject(np.ndarray):
    def __new__(cls, input_array, classname: Incomplete | None = ...): ...
    classname: Incomplete
    def __array_finalize__(self, obj) -> None: ...

class MatlabFunction(np.ndarray):
    def __new__(cls, input_array): ...

class MatlabOpaque(np.ndarray):
    def __new__(cls, input_array): ...

OPAQUE_DTYPE: Incomplete
