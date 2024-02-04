
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional, Self
from numpy import sqrt
from sklearn.metrics import DistanceMetric
from pprint import pformat
from textwrap import indent
import logging



from .dominance_graph import DominanceGraph
from .. dataset.dataset import Dataset
from .. perturbation.adv_region import AdversarialRegion
from .. space.partitioning import Partitions

logger = logging.getLogger(__name__)
@dataclass
class AbstractClassifier:
  distance_metric: DistanceMetric
  partition_tree: Optional[Partitions] = field(default=None)


  def fit(self: Self,
          dataset: Dataset,
          partition_size: int = 10,
          random_state: Optional[int] = None) -> None:

    self.partition_tree = Partitions(dataset, self.distance_metric, partition_size, random_state)

  def get_classification(self: Self,
                         adv_region: AdversarialRegion,
                         k_vals: list[int]) -> dict[int, set[int]]:

    max_k = max(k_vals)
    if self.partition_tree is None:
      raise ValueError("Missing dataset!! Call fit first with a dataset.")

    init_radius: float = adv_region.epsilon*sqrt(adv_region.point.shape[0])

    closer_points = self.partition_tree.query_point(adv_region.point, init_radius, True)

    while closer_points.num_points < max_k:
      radius = self.distance_metric.pairwise([adv_region.point], closer_points.points)[0].max()
      closer_points = self.partition_tree.query_radius(adv_region.point, 2*radius, True)

    logger.debug("\t closer points: ")
    logger.debug('%s\n', indent(pformat(closer_points.points, compact=True),'\t\t'))

    dominance_graph: DominanceGraph = DominanceGraph.build_dominance_graph(adv_region, closer_points, self.distance_metric)
    possible_classifications = dominance_graph.get_neighbors_label(k_vals)

    classifications: dict[int, set[int]] = defaultdict(set)

    for k, possible_labels in possible_classifications.items():
      classification: set[int] = set()

      for labels in possible_labels:
        counter: Counter[int] = Counter(labels)
        max_freq: int = counter.most_common(1)[0][1]
        most_freq_labels: list[int] = [k for k,v in counter.items() if v == max_freq]
        classification = classification | set(most_freq_labels)

      classifications[k] = classification

    return classifications