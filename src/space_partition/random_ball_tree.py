from __future__ import annotations
from collections import deque

from dataclasses import InitVar, dataclass, field
from typing import Iterable,  Optional, Self, Tuple

from .. dataset_loader.dataset import Dataset
from .. space_partition.search_algorithm import find_closest_child_from_point, find_closest_from_ball, search_partitions
from typings.base_types import Array1xM, ArrayNxM, NDVector
import numpy as np
import miniball as mb
from .. utils.hyperplane import Hyperplane
from sklearn.cluster import KMeans
from .. utils.ndball import NDBall
from .. utils.distance import squared_dist

@dataclass
class Leaf:
  dataset: Dataset = field()
  ref_point: Array1xM = field()
  ball: NDBall = field(init=False)

  def __init__(self: Self, dataset: Dataset,
               ref_point: Optional[Array1xM] = None) -> None:

    self.dataset = dataset
    if ref_point is not None:
      self.ref_point = ref_point

  def __post_init__(self: Self) -> None:
    center, radius = mb.get_bounding_ball(self.dataset)
    self.ball = NDBall(center, radius)

@dataclass(init=False)
class Node:
  left_child: 'Node' | Leaf
  right_child: 'Node' | Leaf

  ref_point: Array1xM
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

    const: np.float_  = (np.linalg.norm(self.left_child.ref_point))**2 - \
                        (np.linalg.norm(self.right_child.ref_point))**2

    return Hyperplane(coefs, const)

@dataclass
class RandomBallTree:

  root: 'Node' | Leaf = field(init=False)
  dataset: InitVar[Dataset]
  leaf_size: int = field(default=100)

  def __post_init__(self: Self, dataset: Dataset) -> None:
      self.root = _build_tree(dataset, self.leaf_size);

  def query_point(self: Self, point: Array1xM, init_val: float = 0.0) -> Dataset:

    def enclosing_ball_radius(partition: Leaf) -> np.float_:
      return init_val + squared_dist(point, partition.ball.center) + partition.ball.radius

    partitions: list[Leaf] = search_partitions(deque([self.root]), point, find_closest_child_from_point)

    ball_radius: np.float_ = np.min(list(map(enclosing_ball_radius, partitions)))

    return self.query_radius(NDBall(point, ball_radius))

  def query_radius(self: Self, ball: NDBall) -> Dataset:
    datasets: list[Dataset] = []
    partitions: list[Leaf] = search_partitions(deque([self.root]), ball, find_closest_from_ball)

    for partition in partitions:
      dists = ((partition.dataset.points - ball.center)**2).sum(axis=1)
      datasets.append(partition.dataset[dists <= ball.radius, :])

    return Dataset.vstack(*datasets)


def _build_tree(dataset: Dataset, leaf_size: int) -> Node | Leaf:

  def split_dataset(dataset: Dataset) -> tuple[tuple[NDVector, Dataset], tuple[NDVector, Dataset]]:
    clusters = KMeans(n_clusters=2, n_init='auto').fit(dataset)

    centroids, labels = clusters.cluster_centers_, clusters.labels_

    left_side_points = dataset[labels == 0]
    right_side_points = dataset[labels == 1]

    return (centroids[0], left_side_points), (centroids[1], right_side_points)


  if dataset.num_points <= leaf_size:
    return Leaf(dataset)
  else:
    (l_ref, l_points), (r_ref, r_points) = split_dataset(dataset)
    left_node = _build_tree(l_points, leaf_size)
    right_node = _build_tree(r_points, leaf_size)

  left_node.ref_point = l_ref
  right_node.ref_point = r_ref

  return Node(left_node, right_node)










