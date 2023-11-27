from _typeshed import Incomplete

def spline_filter1d(input, order: int = ..., axis: int = ..., output=..., mode: str = ...): ...
def spline_filter(input, order: int = ..., output=..., mode: str = ...): ...
def geometric_transform(input, mapping, output_shape: Incomplete | None = ..., output: Incomplete | None = ..., order: int = ..., mode: str = ..., cval: float = ..., prefilter: bool = ..., extra_arguments=..., extra_keywords=...): ...
def map_coordinates(input, coordinates, output: Incomplete | None = ..., order: int = ..., mode: str = ..., cval: float = ..., prefilter: bool = ...): ...
def affine_transform(input, matrix, offset: float = ..., output_shape: Incomplete | None = ..., output: Incomplete | None = ..., order: int = ..., mode: str = ..., cval: float = ..., prefilter: bool = ...): ...
def shift(input, shift, output: Incomplete | None = ..., order: int = ..., mode: str = ..., cval: float = ..., prefilter: bool = ...): ...
def zoom(input, zoom, output: Incomplete | None = ..., order: int = ..., mode: str = ..., cval: float = ..., prefilter: bool = ..., *, grid_mode: bool = ...): ...
def rotate(input, angle, axes=..., reshape: bool = ..., output: Incomplete | None = ..., order: int = ..., mode: str = ..., cval: float = ..., prefilter: bool = ...): ...
