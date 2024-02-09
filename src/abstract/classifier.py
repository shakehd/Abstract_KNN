
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional, Self
from numpy import sqrt
from sklearn.metrics import DistanceMetric
from pprint import pformat
from textwrap import indent
import logging



from .dominance_graph import DominanceGraph
from ..dataset.dataset import Dataset
from ..perturbation.adv_region import AdversarialRegion
from ..space.partition_tree import Partitions

logger = logging.getLogger(__name__)
@dataclass
class AbstractClassifier:
  distance_metric: DistanceMetric
  partition_tree: Optional[Partitions] = field(default=None)


  def fit(self: Self,
          dataset: Dataset,
          partition_size: int = 20,
          random_state: Optional[int] = None) -> None:

    self.partition_tree = Partitions(dataset, self.distance_metric, partition_size, random_state)

  def get_classification(self: Self,
                         adv_region: AdversarialRegion,
                         k_vals: list[int]) -> dict[int, set[int]]:

    max_k = max(k_vals)
    if self.partition_tree is None:
      raise ValueError("Missing dataset!! Call fit first with a dataset.")

    init_radius: float = 2*adv_region.epsilon*sqrt(adv_region.point.shape[0])

    closer_points, dists = self.partition_tree.query_point(adv_region.point, init_radius, max_k, True)

    closer_points = closer_points[dists <= dists[max_k-1] + init_radius]
    if closer_points.num_points < max_k:
      logger.error(f'Not enough closer points !!')

    logger.debug("\t closer points: ")
    logger.debug('%s\n', indent(pformat(closer_points.points, compact=True),'\t\t'))

    dominance_graph: DominanceGraph = DominanceGraph.build_dominance_graph(adv_region, closer_points, self.distance_metric)
    possible_classifications = dominance_graph.get_neighbors_label(k_vals)

    return {k:classifications for k, classifications in possible_classifications.items() if k in k_vals}