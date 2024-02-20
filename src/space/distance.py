from enum import Enum, auto
from math import isclose

from sklearn.metrics import DistanceMetric
from src.utils.base_types import Array1xM, NDVector
import numpy as np

class Closer(Enum):
  FIRST   = auto()
  BOTH    = auto()
  SECOND  = auto()


def which_is_closer(target_point: NDVector, fst_point: NDVector,
                    snd_point: NDVector, distance_metric: DistanceMetric) -> Closer:

  left_dist = distance_metric.pairwise([target_point], [fst_point])[0]
  right_dist = distance_metric.pairwise([target_point], [snd_point])[0]

  if isclose(left_dist, right_dist):
    return Closer.BOTH
  else:
    if left_dist > right_dist:
      return Closer.SECOND
    else:
      return Closer.FIRST

def get_closer_manhattan(target_point: NDVector, fst_point: NDVector,
                  snd_point: NDVector,
                  max_distance_delta: float,
                  delta: float,
                  distance_metric: DistanceMetric,
                  max_constraint : float = np.inf) -> Closer:

    fst_dist = distance_metric.pairwise([fst_point], [target_point])[0]
    snd_dist = distance_metric.pairwise([snd_point], [target_point])[0]

    distance_delta = abs(fst_dist - snd_dist)

    if not isclose(distance_delta, max_distance_delta) and \
       distance_delta > max_distance_delta:

      if fst_dist > snd_dist:
        return Closer.SECOND
      else:
        return Closer.FIRST

    else:

      if fst_dist > snd_dist:
        closer_point, further_point, closer = snd_point, fst_point, Closer.SECOND
      else:
        closer_point, further_point, closer = fst_point, snd_point, Closer.FIRST

      threshold = distance_delta / 2
      diff = 0.0
      for ix in range(closer_point.shape[0]):

        if not (closer_point[ix] <= further_point[ix] <= target_point[ix]) and \
           not (target_point[ix] <= further_point[ix] <= closer_point[ix]) and \
           not isclose(diff, max_constraint):

          if closer_point[ix] <=target_point[ix] <= further_point[ix]:
            diff += min(further_point[ix],target_point[ix] + delta) - target_point[ix]

          elif further_point[ix] <= closer_point[ix] <=target_point[ix]:
            diff += max (0, closer_point[ix] - max(further_point[ix],target_point[ix] - delta))

          elif further_point[ix] <=target_point[ix] <= closer_point[ix]:
            diff += target_point[ix] - max(further_point[ix],target_point[ix] - delta)

          elif target_point[ix] <= closer_point[ix] <= further_point[ix]:
            diff += max(0, min(further_point[ix],target_point[ix] + delta) - closer_point[ix])

          diff = np.min([diff, max_constraint])

          if diff >= threshold or isclose(diff, threshold):
            return Closer.BOTH

      return closer