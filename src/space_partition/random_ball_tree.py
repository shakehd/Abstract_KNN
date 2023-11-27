from __future__ import annotations
from collections import deque

from dataclasses import InitVar, dataclass, field
from typing import List, Optional, Self, Tuple
from space_partition.search_algorithm import find_closest_child_from_point, find_closest_from_ball, search_partitions
from base_types import Array1xM, ArrayNxM
import numpy as np
import miniball as mb
from utils.hyperplane import Hyperplane
from scipy.cluster.vq import kmeans2
from utils.ndball import NDBall

from utils.utils import squared_dist

type TNode = Node | Leaf


@dataclass
class Leaf:
  points: ArrayNxM = field()
  ref_point: Array1xM = field()
  ball: NDBall = field(init=False)

  def __init__(self: Self, points: ArrayNxM,
               ref_point: Optional[Array1xM] = None) -> None:

    self.points = points
    if ref_point is not None:
      self.ref_point = ref_point

  def __post_init__(self: Self) -> None:
    center, radius = mb.get_bounding_ball(self.points)
    self.ball = NDBall(center, radius)

@dataclass(init=False)
class Node:
  left_child: TNode
  right_child:  TNode

  ref_point: Array1xM
  axial_hyperplane: Hyperplane

  def __init__(self: Self, left_child: TNode, right_child: TNode,
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

  root: TNode = field(init=False)
  dataset: InitVar[ArrayNxM]
  leaf_size: int = field(default=100)

  def __post_init__(self: Self, dataset: ArrayNxM) -> None:
      self.root = _build_tree(dataset, self.leaf_size);

  def query_point(self: Self, point: Array1xM) -> ArrayNxM:

    def enclosing_ball_radius(partition: Leaf) -> np.float_:
      return squared_dist(point, partition.ball.center) + partition.ball.radius

    partitions: List[Leaf] = search_partitions(deque([self.root]), point, find_closest_child_from_point)

    ball_radius: np.float_ = np.min(list(map(enclosing_ball_radius, partitions)))

    return self.query_radius(NDBall(point, ball_radius))

  def query_radius(self: Self, ball: NDBall) -> ArrayNxM:
    points: List[Array1xM] = []
    partitions: List[Leaf] = search_partitions(deque([self.root]), ball, find_closest_from_ball)

    for partition in partitions:
      dists = ((partition.points - ball.center)**2).sum(axis=1)
      points.append(partition.points[dists <= ball.radius, :])

    return np.vstack(points)


def _build_tree(dataset: ArrayNxM, leaf_size: int) -> TNode:

  def _split_dataset(dataset: ArrayNxM) -> Tuple[Tuple[Array1xM, ArrayNxM], Tuple[Array1xM, ArrayNxM]]:
    centroids, labels = kmeans2(dataset, k = 2, minit='++', iter=1)

    left_side_points = dataset[labels == 0]
    right_side_points = dataset[labels == 1]

    return (centroids[0].reshape(1, -1), left_side_points), \
           (centroids[1].reshape(1, -1), right_side_points)

  nrows: int = dataset.shape[0]

  if nrows <= leaf_size:
    return Leaf(dataset)
  else:
    (l_ref, l_points), (r_ref, r_points) = _split_dataset(dataset)
    left_node = _build_tree(l_points, leaf_size)
    right_node = _build_tree(r_points, leaf_size)

  left_node.ref_point = l_ref
  right_node.ref_point = r_ref

  return Node(left_node, right_node)










