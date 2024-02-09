from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from typing import Optional, Self
import numpy as np
from sklearn.metrics import DistanceMetric
from src.space.search import query_point, query_radius

from src.utils.base_types import ArrayNxM, NDVector
from src.utils.tree import Leaf, Node, build_tree
from src.dataset.dataset import Dataset

@dataclass
class Partitions:
  dataset: Dataset
  distance: DistanceMetric
  leaf_size: int
  random_state: InitVar[Optional[int]] = field(default=None)
  root: Node | Leaf = field(init=False)

  def __post_init__(self: Self, random_state: Optional[int]) -> None:
    self.root = build_tree(self.dataset.points, self.leaf_size, self.distance, random_state)

  def query_point(self: Self, point: NDVector, init_radius: float = 0.0,
                  min_points: int = 7, sorted: bool = False) -> tuple[Dataset, ArrayNxM]:

    partitions: list[Leaf] = query_point(self.root, point, self.distance)

    closer_points: ArrayNxM = np.vstack([self.dataset.points[p.indices] for p in partitions])
    dists: ArrayNxM = np.sort(self.distance.pairwise([point], closer_points)[0])
    ball_radius: float = dists[min_points-1] + init_radius

    return self.query_radius(point, ball_radius, sorted)

  def query_radius(self: Self, point: NDVector, radius: float,
                   sorted: bool = False) -> tuple[Dataset, ArrayNxM]:
    datasets: list[Dataset] = []
    partitions: list[Leaf] = query_radius(self.root, point, radius, self.distance)

    for partition in partitions:
      partition_dataset = self.dataset[partition.indices]
      dists = self.distance.pairwise([point], partition_dataset.points)[0]
      datasets.append(partition_dataset[dists <= radius])

    result = Dataset.vstack(*datasets)

    dists = self.distance.pairwise([point], result.points)[0]
    if sorted:
      sorted_ixs = np.argsort(dists)
      return result[sorted_ixs], dists[sorted_ixs]
    else:
      return result, dists
