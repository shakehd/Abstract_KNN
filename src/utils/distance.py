from enum import Enum, auto
from math import isclose
from typings.base_types import Array1xM, NDVector
import numpy as np

class Selection(Enum):
  FIRST   = auto()
  BOTH    = auto()
  SECOND  = auto()

def squared_dist(first_point: Array1xM, second_point: Array1xM) -> np.float_:
  return np.sum((first_point - second_point)**2)

def which_is_closer(target_point: NDVector, fst_point: NDVector,
                    snd_point: NDVector) -> Selection:
  left_dist = squared_dist(target_point, fst_point)
  right_dist = squared_dist(target_point, snd_point)

  if isclose(left_dist, right_dist):
    return Selection.BOTH
  else:
    if left_dist > right_dist:
      return Selection.SECOND
    else:
      return Selection.FIRST