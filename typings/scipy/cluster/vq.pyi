from typing import Tuple
from typings.base_types import ArrayNxM
from numpy.random import Generator, RandomState

class ClusterError(Exception): ...

def kmeans2(data: ArrayNxM, k: int, iter: int = 10, thresh: float = 1e-5,
            minit: str = 'random', missing: str = 'warn',
            check_finite: bool = True, *,
            seed: None | int | Generator | RandomState = None) -> Tuple[ArrayNxM, ArrayNxM]:
  ...
