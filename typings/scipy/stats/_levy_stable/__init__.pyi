from .._distn_infrastructure import rv_continuous
from _typeshed import Incomplete

class levy_stable_gen(rv_continuous):
    parameterization: str
    pdf_default_method: str
    cdf_default_method: str
    quad_eps: Incomplete
    piecewise_x_tol_near_zeta: float
    piecewise_alpha_tol_near_one: float
    pdf_fft_min_points_threshold: Incomplete
    pdf_fft_grid_spacing: float
    pdf_fft_n_points_two_power: Incomplete
    pdf_fft_interpolation_level: int
    pdf_fft_interpolation_degree: int
    def rvs(self, *args, **kwds): ...
    def pdf(self, x, *args, **kwds): ...
    def cdf(self, x, *args, **kwds): ...

def pdf_from_cf_with_fft(cf, h: float = ..., q: int = ..., level: int = ...): ...

levy_stable: Incomplete
