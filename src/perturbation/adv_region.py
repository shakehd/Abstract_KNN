from dataclasses import dataclass, field
from typing import Any, Self, Sequence
from nptyping import Float
import numpy as np
from src.abstract_domain.interval import Interval

from typings.base_types import NDVector, Integer, Real, String

@dataclass
class AdversarialRegion:
  point: NDVector
  epsilon: float = field(default_factory=float)
  num_feature_ix: Integer = field(default_factory=int)
  adv_region: Sequence[Interval | Real] = field(init=False)

  def __post_init__(self: Self) -> None:
    self.adv_region = list(self.point[:self.num_feature_ix])

    for num_feature in self.point[self.num_feature_ix:]:
      self.adv_region.append(Interval(num_feature - self.epsilon, num_feature + self.epsilon))

  def perturbation_closest_point(self: Self, point: NDVector) -> NDVector:
    closest_point = np.zeros(shape=self.point.shape)

    closest_point[self.num_feature_ix:] = self.adv_region[self.num_feature_ix:]

    for ix in range(self.num_feature_ix, point.shape[0]):
      interval: Interval = self.adv_region[ix] # type: ignore
      closest_point[ix] = min(max(point[ix], interval.lb), interval.ub)

    return closest_point

  def distance_to_point(self: Self, point: NDVector) -> np.float_:
    closest_point = self.perturbation_closest_point(point)

    return np.linalg.norm(closest_point - point)**2

  def __str__(self: Self) -> String:
    repr = ', '.join([str(elem) for elem in self.adv_region])

    return f'[{repr}]'




