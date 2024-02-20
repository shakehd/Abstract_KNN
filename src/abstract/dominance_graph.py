from __future__ import annotations
from collections import Counter, defaultdict, deque, namedtuple
from dataclasses import InitVar, dataclass, field
from typing import  Any, NamedTuple, Optional, Self, Type
from itertools import groupby
import numpy as np
from  pprint import pformat
from textwrap import indent
import logging
from copy import deepcopy
from itertools import combinations, product, chain, repeat



from sklearn.metrics import DistanceMetric
from ..dataset.dataset import Dataset
from ..perturbation.adv_region import AdversarialRegion
from ..space.distance import Closer, which_is_closer


logger = logging.getLogger(__name__)

from src.utils.base_types import NDVector

VertexId = str

@dataclass
class Vertex:
  id: VertexId
  point: Optional[NDVector] = field(default=None)
  label: int = field(default=-1)
  edges: list[VertexId] = field(default_factory=list)
  closer_vertices: set[VertexId] = field(default_factory=set)

class LabelItem(NamedTuple):
  id: str
  label: int
  num: int
  prefix: Counter[tuple[str, int]]

@dataclass
class Item:
  id: str
  num: int = field(default=0)
  vertex: set[VertexId] = field(default_factory=set)
  prefix: dict[str, set[VertexId]] = field(default_factory=dict)


  def add_vertex(self: Self, vertex: VertexId) -> None:
    self.vertex.add(vertex)
    self.num += 1

@dataclass(unsafe_hash=True, order=True, eq=True)
class PathElems:
  num: int
  possible_vertex: frozenset[VertexId]
  graph: InitVar[DominanceGraph]
  all: bool = field(init= False, compare=False, hash=False)
  label_counter: Counter[int] = field(init=False, compare=False, hash=False)

  def __post_init__(self: Self, graph: DominanceGraph) -> None:
    self.all = self.num == len(self.possible_vertex)
    self.label_counter = Counter([graph[v].label for v in self.possible_vertex])

  def incr_occurrence(self: Self, graph: DominanceGraph) -> PathElems:
    if self.num <= len(self.possible_vertex):
      return PathElems(self.num+1, self.possible_vertex, graph)
    else:
      return PathElems(self.num, self.possible_vertex, graph)

  def get_possible_labels(self: Self) -> set[tuple[int,...]]:

    labels: list[int] = [l for label, occurrences in self.label_counter.items()
                           for l in repeat(label, min(occurrences, self.num))]

    return set(combinations(labels, self.num))
@dataclass
class PathSection:
  num: int
  elems: set[PathElems] = field(default_factory=set)

  def set_required_vertices(self: Self, required_vertices: set[VertexId],
                            graph: DominanceGraph) -> None:

    new_items: set[PathElems] = set()
    for item in self.elems:

      if item.possible_vertex == required_vertices:
        return

      remaining_vertices: frozenset[VertexId] = item.possible_vertex - required_vertices
      common_vertices: frozenset[VertexId] = item.possible_vertex & required_vertices
      if common_vertices:
          if item.num - len(common_vertices) > 0:
            new_items.add(PathElems(item.num - len(common_vertices), remaining_vertices, graph))
      else:
        new_items.add(PathElems(item.num, item.possible_vertex, graph))

    new_items.add(PathElems(len(required_vertices), frozenset(required_vertices), graph))
    self.elems = new_items

  def add_occurrence(self: Self, vertex: set[VertexId], graph: DominanceGraph) -> None:

    found_item: Optional[PathElems] = None
    for item in sorted(self.elems):

      if vertex == item.possible_vertex:
        found_item = item
        break

      if item.all:
        vertex = vertex - item.possible_vertex

    if vertex:
      if found_item is not None:
        self.elems.remove(found_item)
        self.elems.add(found_item.incr_occurrence(graph))
      else:
         self.elems.add(PathElems(1, frozenset(vertex), graph))

    self.num += 1

  def get_possible_labels(self: Self) -> set[tuple[int,...]]:

    label_combinations = [elem.get_possible_labels() for elem in self.elems]

    return set(tuple(chain(*labels)) for labels in product(*label_combinations))
@dataclass
class Path:
  sections: dict[str, PathSection]

  def add_item(self: Self, item: Item, graph: DominanceGraph) -> Optional[Path]:

    if item.id in self.sections and self.sections[item.id].num == item.num:
      return None

    new_path: dict[str, PathSection] = deepcopy(self.sections)

    for item_id, vertices in item.prefix.items():

      if not self._requirements_satisfied(item_id, vertices):
        return None

      new_path[item_id].set_required_vertices(vertices, graph)

    if item.id not in new_path:
      new_path[item.id] = PathSection(1, set([PathElems(1, frozenset(item.vertex), graph)]))
    else:
      new_path[item.id].add_occurrence(item.vertex, graph)

    return Path(new_path)

  def get_possible_labels(self: Self) -> set[tuple[int,...]]:

    label_combinations = [section.get_possible_labels() for section in self.sections.values()]

    return set(tuple(chain(*labels)) for labels in product(*label_combinations))

  def _requirements_satisfied(self: Self, item_id: str, vertices: set[VertexId]) -> bool:

    if item_id not in self.sections:
      return False

    if self.sections[item_id].num < len(vertices):
      return False

    if not frozenset.union(*[i.possible_vertex for i in self.sections[item_id].elems]) >= vertices:
      return False

    return True

  @classmethod
  def emptyPath(cls:  type[Path]) -> Path:
    return cls(dict())


@dataclass
class DominanceGraph:
  vertices: dict[VertexId, Vertex]

  def __getitem__(self: Self, key: VertexId) -> Vertex:
    return self.vertices[key]

  def get_neighbors_label(self: Self, k_vals: list[int]) -> dict[int, set[int]]:

    def get_possible_classifications(possible_paths: list[Path]) -> set[int]:
      classifications: set[int] = set()

      for path in possible_paths:
        for neighbor_labels in path.get_possible_labels():

          label_counter = Counter(list(neighbor_labels))
          max_freq: int = label_counter.most_common(1)[0][1]
          most_freq_labels: list[int] = [label for label,v in label_counter.items() if v == max_freq]

          classifications.update(most_freq_labels)

      return classifications

    def extend_paths(paths: list[Path], items: dict[str, Item], graph: DominanceGraph ) -> list[Path]:

      new_paths: list[Path] = []
      to_remove: list[str] = []
      for item in items.values():
        added: bool = False
        for path in paths:

          new_path = path.add_item(item, graph)
          if new_path is not None:
            added = True
            if new_path not in new_paths:
              new_paths.append(new_path)

        if not added:
          to_remove.append(item.id)

      for item_id in to_remove:
        del items[item_id]

      return new_paths

    max_k = max(k_vals)

    possible_paths: dict[int, list[Path]] = dict()
    possible_paths[0] = [Path.emptyPath()]
    vertex_path_item: dict[str, str] = dict()
    possible_path_items: dict[str, Item] = dict()

    result:  dict[int, set[int]] = defaultdict(set)

    graph_vertices: list[Vertex] = [v for id,v in self.vertices.items() if id != 'root' ]
    graph_vertices = sorted(graph_vertices, key=lambda val: len(val.closer_vertices))
    closer_vertices = [v for v in graph_vertices if len(v.closer_vertices) <= max_k]

    k = 1
    for min_length, adj_vertices in groupby(closer_vertices, lambda val: len(val.closer_vertices)):

      if k > max_k:
        break

      while k-1 < min_length:
        possible_paths[k] = extend_paths(possible_paths[k-1], possible_path_items, self)
        result[k] = get_possible_classifications(possible_paths[k])
        k += 1

      for vertex in adj_vertices:
        path_item_id = f'{min_length}-{hash(frozenset(vertex.closer_vertices))}'
        vertex_path_item[vertex.id] = path_item_id
        if path_item_id not in possible_path_items:

          prefix: defaultdict[str, set[VertexId]]  = defaultdict(set)
          for vertex_id in vertex.closer_vertices:
            prefix[vertex_path_item[vertex_id]].add(self[vertex_id].id)

          possible_path_items[path_item_id] = Item(id=path_item_id, num=1,
                                                    vertex=set([vertex.id]),
                                                    prefix=prefix)#type: ignore
        else:
          possible_path_items[path_item_id].add_vertex(vertex.id)

      possible_paths[k] = extend_paths(possible_paths[k-1], possible_path_items, self)
      result[k] = get_possible_classifications(possible_paths[k])
      k += 1

    while k-1 <= max_k:
      possible_paths[k] = extend_paths(possible_paths[k-1], possible_path_items, self)
      result[k] = get_possible_classifications(possible_paths[k])
      k += 1

    return result

  @classmethod
  def build_dominance_graph(cls: Type[DominanceGraph],
                            adv_region: AdversarialRegion,
                            dataset: Dataset,
                            distance_metric: DistanceMetric,
                            max_path_length: int = 7) -> DominanceGraph:


    dom_matrix: dict[VertexId, Vertex] = dict(
      [(str(i), Vertex(str(i), dataset.points[i],  dataset.labels[i])) for i in range(dataset.num_points)]
    )
    initial_vertices: set[int] = set(range(dataset.num_points))

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

    root_edges: list[VertexId]= [str(i) for i in initial_vertices]
    dom_matrix['root'] = Vertex('root', edges=root_edges)

    logger.debug("\t dominance graph: \n")
    logger.debug('%s\n', indent(pformat(dom_matrix, compact=True),'\t\t'))
    return cls(dom_matrix)