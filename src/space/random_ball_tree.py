from __future__ import annotations
from collections import deque

from dataclasses import InitVar, dataclass
from typing import  Optional, Self
from sklearn.metrics import DistanceMetric
import kmedoids

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

def build_tree(dataset: Dataset, leaf_size: int, distance: DistanceMetric,
              random_state: Optional[int], max_retries: int = 5) -> Node | Leaf:

  dist_matrix = distance.pairwise(dataset.points)

  def remove_row_column(array: ArrayNxM, to_remove: NDVector) -> ArrayNxM:

    idx = list(set(range(array.shape[0])).difference(to_remove))
    return array[np.ix_(idx, idx)]

  def is_imbalanced(fst_size: int, snd_size: int) -> bool:

    ratio: float = fst_size / (fst_size + snd_size)

    return max(ratio, 1-ratio) > 0.85

  def _go(dist_matrix: ArrayNxM, dataset: Dataset, medoid: Optional[int] = None) -> Node | Leaf:

    if dataset.num_points <= leaf_size:

      if medoid is None:

        cluster = kmedoids.fasterpam(dist_matrix, 1, init='random', random_state=random_state)
        medoid = cluster.medoids[0]

      radius = max(dist_matrix[medoid])
      return Leaf(dataset, dataset.points[medoid], radius)

    else:

      tries = 0
      while tries < max_retries:
        clusters = kmedoids.fasterpam(dist_matrix, 2, init='random', random_state=random_state)

        fst_cluster = dataset[clusters.labels == 0]
        snd_cluster = dataset[clusters.labels == 1]

        if not is_imbalanced(fst_cluster.num_points, snd_cluster.num_points):
          break

        tries += 1

      left_node = _go(remove_row_column(dist_matrix, np.where(clusters.labels == 1)[0]),
                      fst_cluster,
                      int(clusters.medoids[0] - np.count_nonzero(clusters.labels[:clusters.medoids[0]])))
      right_node = _go(remove_row_column(dist_matrix, np.where(clusters.labels == 0)[0]),
                      snd_cluster,
                      int(clusters.medoids[1] - np.count_nonzero(clusters.labels[:clusters.medoids[1]] == 0)))

      return Node(left_node, right_node, dataset.points[medoid])

  return _go(dist_matrix, dataset)












