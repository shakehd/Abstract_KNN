from typings.base_types import Array1xM
import numpy as np


def squared_dist(first_point: Array1xM, second_point: Array1xM) -> np.float_:
  return ((first_point - second_point)**2).sum()
