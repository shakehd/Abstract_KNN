from dataclasses import dataclass, field
from typing import Iterator, Self, Sequence
from itertools import repeat, product, chain
import numpy as np

from src.dataset.dataset import DatasetProps

from ..utils.base_types import Array1xN, ArrayNxM, NDVector
from ..abstract.domain.interval import Interval
from ..space.distance import Closer
from ..space.hyperplane import Hyperplane

@dataclass
class AdvRegion:
  point: NDVector
  epsilon: float = field(default_factory=float)
  num_adv_region: list[Interval] = field(init=False)

  def __post_init__(self: Self) -> None:
    self.num_adv_region = []

    for num_feature in self.point[DatasetProps.num_features_start_ix:]:
      self.num_adv_region.append(Interval(max(num_feature - self.epsilon, 0.0),
                                      min(num_feature + self.epsilon, 1.0)))

  def get_closer(self: Self, bisector: Hyperplane) -> Closer:
    point_side = np.sign(bisector(self.point))

    if point_side == 0:
      return Closer.BOTH

    if point_side > 0 :
      dir = -bisector.coefficients[DatasetProps.num_features_start_ix:].copy()
      closer = Closer.SECOND
    else:
      dir = bisector.coefficients[DatasetProps.num_features_start_ix:].copy()
      closer = Closer.FIRST

    dir = np.hstack([np.zeros((DatasetProps.num_features_start_ix, )), dir])

    continuous_part = dir[DatasetProps.num_features_start_ix:]
    continuous_part[continuous_part == 0] = 1
    target_vertex = self.point + np.sign(dir)*self.epsilon

    if point_side != np.sign(bisector(target_vertex)):
      return Closer.BOTH
    else:
      return closer

  def get_bounds(self: Self) -> Sequence[tuple[float, float| None]]:
    bounds: list[tuple[float, float | None]] = []

    for cat_feature in DatasetProps.cat_features.values():
      if cat_feature.size == 2:
         bounds.append((0, None))
      else:
         bounds += list((repeat((0, None), cat_feature.size)))

    return bounds + [(interval.lb, interval.ub) for interval in self.num_adv_region]

  def get_equality_constraints(self: Self) -> tuple[ArrayNxM, Array1xN]:
    eq_lhs: ArrayNxM = np.zeros((len(DatasetProps.cat_features), DatasetProps.columns))
    eq_rhs: list[float] = []
    for ix in range(len(DatasetProps.cat_features)):
      eq_lhs[ix][ix] = 1.0
      eq_rhs.append(self.point[ix])

    return eq_lhs, np.array(eq_rhs)

@dataclass
class Perturbation:
  point: NDVector
  epsilon: float = field(default_factory=float)
  num_adv_region: list[Interval] = field(init=False)

  def __post_init__(self: Self) -> None:
    self.num_adv_region = []

    for num_feature in self.point[DatasetProps.num_features_start_ix:]:
      self.num_adv_region.append(Interval(max(num_feature - self.epsilon, 0.0),
                                      min(num_feature + self.epsilon, 1.0)))

  def get_adversarial_regions(self: Self) -> Iterator[AdvRegion]:
    cat_possible_values: list[list[list[float]]] = []

    cat_to_perturb = [cat for cat in DatasetProps.cat_features.values()
                          if cat.perturb]

    if cat_to_perturb:
      fixed_cat_start_idx: int = 0
      for cat in cat_to_perturb:

        if cat.size == 1:
          cat_possible_values.append([[1.0]])
          fixed_cat_start_idx +=1

        elif cat.size == 2:
          cat_possible_values.append([[0.0], [1.0]])
          fixed_cat_start_idx +=1

        else:
          cat_possible_values.append([[0.0] * i + [1.0] + [0.0] * (cat.size - i - 1)
                                                  for i in range(cat.size)])
          fixed_cat_start_idx += cat.size

      for combination in product(*cat_possible_values):
        point: NDVector = np.array(list(chain(
          *combination,
          self.point[fixed_cat_start_idx:],
        )))

        yield AdvRegion(point, self.epsilon)
    else:
      yield AdvRegion(self.point, self.epsilon)