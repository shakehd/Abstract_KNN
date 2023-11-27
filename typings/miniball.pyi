from typing import Tuple
from typings.base_types import Array1xM, ArrayNxM
from numpy.random import Generator, default_rng

from numpy import float_


__version__: str

def get_circumsphere(S: ArrayNxM) -> Tuple[Array1xM, float_]:
  ...
def get_bounding_ball(S: ArrayNxM, epsilon: float=1e-7, rng: Generator= default_rng()) -> Tuple[Array1xM, float_]:
  ...