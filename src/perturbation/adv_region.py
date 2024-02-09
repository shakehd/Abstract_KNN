from dataclasses import dataclass, field
from typing import Any, Self, Sequence
from nptyping import Float
import numpy as np
from sklearn.metrics import DistanceMetric
from ..abstract.domain.interval import Interval
from ..space.distance import Closer, get_closer_with_l1, which_is_closer

from src.utils.base_types import NDVector

@dataclass
class AdversarialRegion:
  point: NDVector
  epsilon: float = field(default_factory=float)
  num_feature_starting_ix: int = field(default_factory=int)
  adv_region: Sequence[Interval | float] = field(init=False)

  def __post_init__(self: Self) -> None:
    self.adv_region = list(self.point[:self.num_feature_starting_ix])

    for num_feature in self.point[self.num_feature_starting_ix:]:
      self.adv_region.append(Interval(max(num_feature - self.epsilon, 0.0), min(num_feature + self.epsilon, 1.0)))

  def get_closer(self: Self, fst_point: NDVector,
                   snd_point: NDVector, distance_metric: DistanceMetric) -> Closer:

    if 'EuclideanDistance' in type(distance_metric).__name__:

      closer = which_is_closer(self.point, fst_point, snd_point, distance_metric)
      match  closer:

        case Closer.BOTH:
          return Closer.BOTH

        case Closer.FIRST:
          dir = snd_point - fst_point

        case Closer.SECOND:
          dir = fst_point - snd_point

      dir[dir == 0] = 1
      target_vertex = self.point + np.sign(dir)*self.epsilon

      if closer != which_is_closer(target_vertex, fst_point, snd_point, distance_metric):
        return Closer.BOTH
      else:
        return closer

    elif 'Manhattan' in type(distance_metric).__name__:
          return get_closer_with_l1(self.point, fst_point, snd_point,
                                    2*self.epsilon*np.sqrt(self.point.shape[0]),
                                    self.epsilon, distance_metric,
                                    self.epsilon*self.point.shape[0])

    else:
        raise ValueError(f'distance metric {type(distance_metric).__name__} not supported')



  def perturbation_closest_point(self: Self, point: NDVector) -> NDVector:
    closest_point = np.zeros(shape=self.point.shape)

    closest_point[:self.num_feature_starting_ix] = self.adv_region[:self.num_feature_starting_ix]

    for ix in range(self.num_feature_starting_ix, point.shape[0]):
      interval: Interval = self.adv_region[ix] # type: ignore
      closest_point[ix] = min(max(point[ix], interval.lb), interval.ub)

    return closest_point

  # # def distance_to_point(self: Self, point: NDVector) -> float:
  # #   closest_point = self.perturbation_closest_point(point)

  #   return np.linalg.norm(closest_point - point)**2

  def __str__(self: Self) -> str:
    repr = ', '.join([str(elem) for elem in self.adv_region])

    return f'[{repr}]'




