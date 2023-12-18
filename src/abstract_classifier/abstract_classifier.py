
from collections import Counter
from dataclasses import dataclass, field
from typing import Self
from numpy import sqrt

from .dominance_graph import DominanceGraph
from .. dataset.dataset import Dataset
from typings.base_types import Number
from .. perturbation.adv_region import AdversarialRegion
from .. space_partition.random_ball_tree import RandomBallTree


@dataclass
class AbstractClassifier:
  k: int = field(default=7)
  partition_size: int = field(default=100)
  partition_tree: RandomBallTree = field(init=False)

  def fit(self: Self, dataset: Dataset) -> None:
    self.partition_tree = RandomBallTree(dataset)

  def get_classification(self: Self,
                         adv_region: AdversarialRegion) -> set[Number]:

    init_val: float = sqrt(adv_region.point.shape[1]) * adv_region.epsilon
    points = self.partition_tree.query_point(adv_region.point, init_val)

    dominance_graph: DominanceGraph = DominanceGraph.build_dominance_graph(adv_region, points)
    possible_labels = dominance_graph.get_neighbors(self.k)

    classification: set[Number] = set()

    for labels in possible_labels:
      counter: Counter[Number] = Counter(labels)
      max_freq: int = counter.most_common(1)[0][1]
      most_freq_labels: list[Number] = [k for k,v in counter.items() if v == max_freq]
      classification = classification | set(most_freq_labels)

    return classification