from __future__ import annotations
from collections import deque

from dataclasses import InitVar, dataclass
from typing import  Optional, Self
from sklearn.metrics import DistanceMetric
import kmedoids

from src.space.clustering import two_means

from .. dataset.dataset import Dataset
from typings.base_types import Array1xM, ArrayNxM, NDVector
import numpy as np
from .hyperplane import Hyperplane


@dataclass(frozen=True)
class Ball:
  center: NDVector
  radius: float

@dataclass
class Leaf:
  dataset: Dataset
  indices: NDVector
  center: InitVar[NDVector]
  radius: InitVar[float]


  def __post_init__(self: Self, center: NDVector, radius: float) -> None:
    self.ball = Ball(center, radius)

  @property
  def ref_point(self: Self) -> NDVector:
    return self.ball.center;

@dataclass(init=False)
class Node:
  left_child: 'Node' | Leaf
  right_child: 'Node' | Leaf

  ref_point: NDVector
  axial_hyperplane: Hyperplane

  def __init__(self: Self, left_child: 'Node' | Leaf, right_child: 'Node' | Leaf,
               ref_point: Optional[Array1xM] = None) -> None:
    self.left_child = left_child
    self.right_child = right_child

    if ref_point is not None:
      self.ref_point = ref_point

    self.axial_hyperplane = self._build_axial_hyperplane()

  def _build_axial_hyperplane(self: Self) -> Hyperplane:

    coefs: Array1xM = 2 * (self.left_child.ref_point - self.right_child.ref_point)

    const: float  = (self.left_child.ref_point**2).sum() - \
                        (self.right_child.ref_point**2).sum()

    return Hyperplane(coefs, const)

def build_tree(dataset: ArrayNxM, leaf_size: int, distance_metric: DistanceMetric,
                random_state: Optional[int] = None) -> Node | Leaf:

  def _go(dataset: ArrayNxM, indices: NDVector, ref_point: Optional[NDVector] = None) -> Node | Leaf:

    if len(indices) <= leaf_size:

      points= dataset[indices]

      if ref_point is None:
        if 'Euclidean' in type(distance_metric).__name__:
          ref_point = np.mean(points, axis=0)

        if 'Manhattan' in type(distance_metric).__name__:
          ref_point = np.median(points, axis=0)

      radius = np.max(distance_metric.pairwise([ref_point], points))
      return Leaf(Dataset(np.zeros(1), np.zeros(1), 0), indices, ref_point, radius) #type: ignore

    else:
      cluster = two_means(dataset, indices, distance_metric, random_state)

      left_node = _go(dataset, cluster.left_indices, cluster.left_center)
      right_node = _go(dataset, cluster.right_indices, cluster.right_center)

      return Node(left_node, right_node, ref_point)

  return _go(dataset, np.arange(dataset.shape[0]))





