from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import  Optional, Self, Type
from itertools import permutations
import numpy as np
from  pprint import pformat
from textwrap import indent
import logging


from sklearn.metrics import DistanceMetric
from .. dataset.dataset import Dataset
from .. perturbation.adv_region import AdversarialRegion
from ..space.distance import Closer, which_is_closer


logger = logging.getLogger(__name__)

from typings.base_types import Integer, NDVector, Number, String

Id = String

@dataclass
class Vertex:
  id: Id
  point: Optional[NDVector] = field(default=None)
  label: int = field(default=-1)
  edges: list[Id] = field(default_factory=list)
  closer_vertices: set[Id] = field(default_factory=set)


@dataclass
class DominanceGraph:
  vertices: dict[Id, Vertex]

  def __getitem__(self: Self, key: Id) -> Vertex:
    return self.vertices[key]


  def get_neighbors_label(self: Self, k_vals: list[int]) -> dict[int, list[list[int]]]:

    queue: deque[list[Id]] = deque([[v] for v in self['root'].edges])

    max_k: int = max(k_vals)
    possible_neighbors_label: defaultdict[int, list[list[int]]] = defaultdict(list)


    while True:
      try:
        neighbors: list[Id] = queue.popleft()
        num_neighbors = len(neighbors)

        if num_neighbors > max_k:
          continue

        if num_neighbors in k_vals:
           possible_neighbors_label[num_neighbors].append([self[id].label for id in neighbors])

        frontier_vertex_id: Id = neighbors[-1]

        for adj_id in self[frontier_vertex_id].edges:
          missing_ancestor: bool = bool(self[adj_id].closer_vertices) and \
                                  (not self[adj_id].closer_vertices <= set(neighbors))
          circular_path: bool = adj_id in neighbors

          if not missing_ancestor and not circular_path:
            queue.append(neighbors + [adj_id])

      except IndexError:
        break

    return possible_neighbors_label


  @classmethod
  def build_dominance_graph(cls: Type[DominanceGraph],
                            adv_region: AdversarialRegion,
                            dataset: Dataset,
                            distance_metric: DistanceMetric,
                            max_path_length: int = 7) -> DominanceGraph:


    dom_matrix: dict[String, Vertex] = dict(
      [(str(i), Vertex(str(i), dataset.points[i],  dataset.labels[i])) for i in range(dataset.num_points)]
    )
    initial_vertices: set[Integer] = set(range(dataset.num_points))

    for i in range(dataset.num_points):

      if len(dom_matrix[str(i)].closer_vertices) >= max_path_length:
        initial_vertices.discard(i)

      for j in range(i+1, dataset.num_points):
        match adv_region.get_closer(dataset.points[i], dataset.points[j], distance_metric):

          case Closer.FIRST:
            dom_matrix[str(i)].edges.append(str(j))
            dom_matrix[str(j)].closer_vertices.add(str(i))
            initial_vertices.discard(j)

          case Closer.SECOND:
            dom_matrix[str(j)].edges.append(str(i))
            dom_matrix[str(i)].closer_vertices.add(str(j))
            initial_vertices.discard(i)

          case Closer.BOTH:
            dom_matrix[str(i)].edges.append(str(j))
            dom_matrix[str(j)].edges.append(str(i))

    root_edges: list[String]= [str(i) for i in initial_vertices]
    dom_matrix['root'] = Vertex('root', edges=root_edges)

    logger.debug("\t dominance graph: \n")
    logger.debug('%s\n', indent(pformat(dom_matrix, compact=True),'\t\t'))
    return cls(dom_matrix)