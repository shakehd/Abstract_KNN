from __future__ import annotations
from collections import Counter, defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from typing import  Any, NamedTuple, Optional, Self, Type
from itertools import groupby
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

class LabelItem(NamedTuple):
  id: int
  label: int
  num: int
  prefix: Counter[tuple[int, int]]
@dataclass
class DominanceGraph:
  vertices: dict[Id, Vertex]

  def __getitem__(self: Self, key: Id) -> Vertex:
    return self.vertices[key]


  def get_neighbors_label(self: Self, k_vals: list[int]) -> dict[int, set[int]]:

    def can_add_label(label_item: LabelItem, labels: Counter[tuple[int, int]]) -> bool:

      return labels[(label_item.id, label_item.label)] < label_item.num and \
             labels >= Counter(dict(label_item.prefix))

    def extend_label_seq(possible_labels: list[LabelItem],
                         possible_neighbor_labels: dict[int, list[Counter[tuple[int, int]]]],
                         k: int) -> None:

      to_remove: list[LabelItem] = list()
      for label_item in possible_labels:
        added = False
        for neighbor_labels in possible_neighbor_labels[k -1]:

          if can_add_label(label_item, neighbor_labels):

            new_label_counter = neighbor_labels + Counter([(label_item.id,label_item.label)])
            if not new_label_counter in possible_neighbor_labels[k]:
              possible_neighbor_labels[k].append(new_label_counter)
            added = True

        if not added:
          to_remove.append(label_item)
      if to_remove:
        possible_labels = [item for item in possible_labels if item not in to_remove]


    def get_possible_classifications(possible_neighbor_labels: list[Counter[tuple[int, int]]]) -> set[int]:
      classifications: set[int] = set()

      for neighbor_labels in possible_neighbor_labels:
        label_counter = Counter([elem[1] for elem in neighbor_labels.elements()])
        max_freq: int = label_counter.most_common(1)[0][1]
        most_freq_labels: list[int] = [label for label,v in label_counter.items() if v == max_freq]
        classifications.update(most_freq_labels)

      return classifications

    max_k = max(k_vals)
    possible_neighbor_labels: dict[int, list[Counter[tuple[int, int]]]] = defaultdict(list)
    possible_neighbor_labels[0] = [Counter()]
    possible_labels: list[LabelItem] = list()
    vertex_item: dict[str, int] = dict()

    result:  dict[int, set[int]] = defaultdict(set)

    all_vertices = [v for id,v in self.vertices.items() if id != 'root' ]
    sorted_vertices:list[Vertex] = sorted(all_vertices, key=lambda val: len(val.closer_vertices))
    k = 1
    id = 1
    for min_length, neighbors in groupby(sorted_vertices, lambda val: len(val.closer_vertices)):

      if k > max_k:
        break

      while k-1 < min_length:
        extend_label_seq(possible_labels, possible_neighbor_labels, k)
        result[k] = get_possible_classifications(possible_neighbor_labels[k])
        k += 1

      counter: Counter[tuple[int, tuple[tuple[tuple[int, int], int], ...]]] = Counter()
      for neighbor in neighbors:
        vertex_item[neighbor.id] = id
        req_items = Counter([(vertex_item[id], self[id].label) for id in neighbor.closer_vertices])
        counter.update([(neighbor.label, tuple(list(req_items.items())))])

      for (label, req), count in counter.items():
        possible_labels.append(LabelItem(id, label, count, Counter(dict(req))))


      extend_label_seq(possible_labels, possible_neighbor_labels, k)
      result[k] = get_possible_classifications(possible_neighbor_labels[k])
      id += 1
      k += 1

    while k-1 <= max_k:
      extend_label_seq(possible_labels, possible_neighbor_labels, k)
      result[k] = get_possible_classifications(possible_neighbor_labels[k])
      k += 1

    return result

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