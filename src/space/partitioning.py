from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from typing import Optional, Self
import numpy as np
from sklearn.metrics import DistanceMetric
from src.space.search import query_point, query_radius

from typings.base_types import NDVector
from src.space.random_ball_tree import Leaf, Node, build_tree
from src.dataset.dataset import Dataset

@dataclass
class Partitions:
  dataset: InitVar[Dataset]
  distance: DistanceMetric
  leaf_size: int
  random_state: InitVar[Optional[int]] = field(default=None)
  root: Node | Leaf = field(init=False)

  def __post_init__(self: Self, dataset: Dataset, random_state: Optional[int]) -> None:
      self.root = build_tree(dataset, self.leaf_size, self.distance, random_state);

  def query_point(self: Self, point: NDVector, init_radius: float = 0.0,
                  sorted: bool = False) -> Dataset:

    def enclosing_ball_radius(partition: Leaf) -> float:
      return init_radius + self.distance.pairwise([point], [partition.ref_point])[0] + partition.ball.radius

    partitions: list[Leaf] = query_point(self.root, point, self.distance)

    ball_radius: float = np.min(list(map(enclosing_ball_radius, partitions)))

    return self.query_radius(point, ball_radius, sorted)

  def query_radius(self: Self, point: NDVector, radius: float,
                   sorted: bool = False) -> Dataset:
    datasets: list[Dataset] = []
    partitions: list[Leaf] = query_radius(self.root, point, radius, self.distance)

    for partition in partitions:
      dists = self.distance.pairwise([point], partition.dataset.points)[0]
      datasets.append(partition.dataset[dists <= radius])

    result = Dataset.vstack(*datasets)

    if sorted:
      dists = self.distance.pairwise([point], result.points)[0]
      return result[np.argsort(dists)]
    else:
      return result
