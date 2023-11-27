from ._distn_infrastructure import rv_discrete
from _typeshed import Incomplete

class binom_gen(rv_discrete): ...

binom: Incomplete

class bernoulli_gen(binom_gen): ...

bernoulli: Incomplete

class betabinom_gen(rv_discrete): ...

betabinom: Incomplete

class nbinom_gen(rv_discrete): ...

nbinom: Incomplete

class geom_gen(rv_discrete): ...

geom: Incomplete

class hypergeom_gen(rv_discrete): ...

hypergeom: Incomplete

class nhypergeom_gen(rv_discrete): ...

nhypergeom: Incomplete

class logser_gen(rv_discrete): ...

logser: Incomplete

class poisson_gen(rv_discrete): ...

poisson: Incomplete

class planck_gen(rv_discrete): ...

planck: Incomplete

class boltzmann_gen(rv_discrete): ...

boltzmann: Incomplete

class randint_gen(rv_discrete): ...

randint: Incomplete

class zipf_gen(rv_discrete): ...

zipf: Incomplete

class zipfian_gen(rv_discrete): ...

zipfian: Incomplete

class dlaplace_gen(rv_discrete): ...

dlaplace: Incomplete

class skellam_gen(rv_discrete): ...

skellam: Incomplete

class yulesimon_gen(rv_discrete): ...

yulesimon: Incomplete

class _nchypergeom_gen(rv_discrete):
    rvs_name: Incomplete
    dist: Incomplete

class nchypergeom_fisher_gen(_nchypergeom_gen):
    rvs_name: str
    dist: Incomplete

nchypergeom_fisher: Incomplete

class nchypergeom_wallenius_gen(_nchypergeom_gen):
    rvs_name: str
    dist: Incomplete

nchypergeom_wallenius: Incomplete
