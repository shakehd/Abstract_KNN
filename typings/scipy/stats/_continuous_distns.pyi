from ._distn_infrastructure import rv_continuous
from _typeshed import Incomplete
from scipy.stats._warnings_errors import FitError

class ksone_gen(rv_continuous): ...

ksone: Incomplete

class kstwo_gen(rv_continuous): ...

kstwo: Incomplete

class kstwobign_gen(rv_continuous): ...

kstwobign: Incomplete

class norm_gen(rv_continuous):
    def fit(self, data, **kwds): ...

norm: Incomplete

class alpha_gen(rv_continuous): ...

alpha: Incomplete

class anglit_gen(rv_continuous): ...

anglit: Incomplete

class arcsine_gen(rv_continuous): ...

arcsine: Incomplete

class FitDataError(ValueError):
    args: Incomplete
    def __init__(self, distr, lower, upper) -> None: ...

class FitSolverError(FitError):
    args: Incomplete
    def __init__(self, mesg) -> None: ...

class beta_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

beta: Incomplete

class betaprime_gen(rv_continuous): ...

betaprime: Incomplete

class bradford_gen(rv_continuous): ...

bradford: Incomplete

class burr_gen(rv_continuous): ...

burr: Incomplete

class burr12_gen(rv_continuous): ...

burr12: Incomplete

class fisk_gen(burr_gen): ...

fisk: Incomplete

class cauchy_gen(rv_continuous): ...

cauchy: Incomplete

class chi_gen(rv_continuous): ...

chi: Incomplete

class chi2_gen(rv_continuous): ...

chi2: Incomplete

class cosine_gen(rv_continuous): ...

cosine: Incomplete

class dgamma_gen(rv_continuous): ...

dgamma: Incomplete

class dweibull_gen(rv_continuous): ...

dweibull: Incomplete

class expon_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

expon: Incomplete

class exponnorm_gen(rv_continuous): ...

exponnorm: Incomplete

class exponweib_gen(rv_continuous): ...

exponweib: Incomplete

class exponpow_gen(rv_continuous): ...

exponpow: Incomplete

class fatiguelife_gen(rv_continuous): ...

fatiguelife: Incomplete

class foldcauchy_gen(rv_continuous): ...

foldcauchy: Incomplete

class f_gen(rv_continuous): ...

f: Incomplete

class foldnorm_gen(rv_continuous): ...

foldnorm: Incomplete

class weibull_min_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

weibull_min: Incomplete

class truncweibull_min_gen(rv_continuous): ...

truncweibull_min: Incomplete

class weibull_max_gen(rv_continuous): ...

weibull_max: Incomplete

class genlogistic_gen(rv_continuous): ...

genlogistic: Incomplete

class genpareto_gen(rv_continuous): ...

genpareto: Incomplete

class genexpon_gen(rv_continuous): ...

genexpon: Incomplete

class genextreme_gen(rv_continuous): ...

genextreme: Incomplete

class gamma_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

gamma: Incomplete

class erlang_gen(gamma_gen):
    def fit(self, data, *args, **kwds): ...

erlang: Incomplete

class gengamma_gen(rv_continuous): ...

gengamma: Incomplete

class genhalflogistic_gen(rv_continuous): ...

genhalflogistic: Incomplete

class genhyperbolic_gen(rv_continuous): ...

genhyperbolic: Incomplete

class gompertz_gen(rv_continuous): ...

gompertz: Incomplete

class gumbel_r_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

gumbel_r: Incomplete

class gumbel_l_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

gumbel_l: Incomplete

class halfcauchy_gen(rv_continuous): ...

halfcauchy: Incomplete

class halflogistic_gen(rv_continuous): ...

halflogistic: Incomplete

class halfnorm_gen(rv_continuous): ...

halfnorm: Incomplete

class hypsecant_gen(rv_continuous): ...

hypsecant: Incomplete

class gausshyper_gen(rv_continuous): ...

gausshyper: Incomplete

class invgamma_gen(rv_continuous): ...

invgamma: Incomplete

class invgauss_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

invgauss: Incomplete

class geninvgauss_gen(rv_continuous): ...

geninvgauss: Incomplete

class norminvgauss_gen(rv_continuous): ...

norminvgauss: Incomplete

class invweibull_gen(rv_continuous): ...

invweibull: Incomplete

class johnsonsb_gen(rv_continuous): ...

johnsonsb: Incomplete

class johnsonsu_gen(rv_continuous): ...

johnsonsu: Incomplete

class laplace_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

laplace: Incomplete

class laplace_asymmetric_gen(rv_continuous): ...

laplace_asymmetric: Incomplete

class levy_gen(rv_continuous): ...

levy: Incomplete

class levy_l_gen(rv_continuous): ...

levy_l: Incomplete

class logistic_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

logistic: Incomplete

class loggamma_gen(rv_continuous): ...

loggamma: Incomplete

class loglaplace_gen(rv_continuous): ...

loglaplace: Incomplete

class lognorm_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

lognorm: Incomplete

class gibrat_gen(rv_continuous): ...

gibrat: Incomplete

class maxwell_gen(rv_continuous): ...

maxwell: Incomplete

class mielke_gen(rv_continuous): ...

mielke: Incomplete

class kappa4_gen(rv_continuous): ...

kappa4: Incomplete

class kappa3_gen(rv_continuous): ...

kappa3: Incomplete

class moyal_gen(rv_continuous): ...

moyal: Incomplete

class nakagami_gen(rv_continuous): ...

nakagami: Incomplete

class ncx2_gen(rv_continuous): ...

ncx2: Incomplete

class ncf_gen(rv_continuous): ...

ncf: Incomplete

class t_gen(rv_continuous): ...

t: Incomplete

class nct_gen(rv_continuous): ...

nct: Incomplete

class pareto_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

pareto: Incomplete

class lomax_gen(rv_continuous): ...

lomax: Incomplete

class pearson3_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

pearson3: Incomplete

class powerlaw_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

powerlaw: Incomplete

class powerlognorm_gen(rv_continuous): ...

powerlognorm: Incomplete

class powernorm_gen(rv_continuous): ...

powernorm: Incomplete

class rdist_gen(rv_continuous): ...

rdist: Incomplete

class rayleigh_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

rayleigh: Incomplete

class reciprocal_gen(rv_continuous):
    fit_note: str
    def fit(self, data, *args, **kwds): ...

loguniform: Incomplete
reciprocal: Incomplete

class rice_gen(rv_continuous): ...

rice: Incomplete

class recipinvgauss_gen(rv_continuous): ...

recipinvgauss: Incomplete

class semicircular_gen(rv_continuous): ...

semicircular: Incomplete

class skewcauchy_gen(rv_continuous): ...

skewcauchy: Incomplete

class skewnorm_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

skewnorm: Incomplete

class trapezoid_gen(rv_continuous): ...

trapezoid: Incomplete
trapz: Incomplete

class triang_gen(rv_continuous): ...

triang: Incomplete

class truncexpon_gen(rv_continuous): ...

truncexpon: Incomplete

class truncnorm_gen(rv_continuous): ...

truncnorm: Incomplete

class truncpareto_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

truncpareto: Incomplete

class tukeylambda_gen(rv_continuous): ...

tukeylambda: Incomplete

class FitUniformFixedScaleDataError(FitDataError):
    args: Incomplete
    def __init__(self, ptp, fscale) -> None: ...

class uniform_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

uniform: Incomplete

class vonmises_gen(rv_continuous):
    def rvs(self, *args, **kwds): ...
    def expect(self, func: Incomplete | None = ..., args=..., loc: int = ..., scale: int = ..., lb: Incomplete | None = ..., ub: Incomplete | None = ..., conditional: bool = ..., **kwds): ...
    def fit(self, data, *args, **kwds): ...

vonmises: Incomplete
vonmises_line: Incomplete

class wald_gen(invgauss_gen): ...

wald: Incomplete

class wrapcauchy_gen(rv_continuous): ...

wrapcauchy: Incomplete

class gennorm_gen(rv_continuous): ...

gennorm: Incomplete

class halfgennorm_gen(rv_continuous): ...

halfgennorm: Incomplete

class crystalball_gen(rv_continuous): ...

crystalball: Incomplete

class argus_gen(rv_continuous): ...

argus: Incomplete

class rv_histogram(rv_continuous):
    def __init__(self, histogram, *args, density: Incomplete | None = ..., **kwargs) -> None: ...

class studentized_range_gen(rv_continuous): ...

studentized_range: Incomplete

class rel_breitwigner_gen(rv_continuous):
    def fit(self, data, *args, **kwds): ...

rel_breitwigner: Incomplete
