from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import  Any, Iterable, Optional, Self, Type
from  pprint import pformat
from textwrap import indent
import logging
from copy import deepcopy
from itertools import combinations, product, groupby
from functools import cached_property, reduce
from sklearn.metrics import DistanceMetric

from ..dataset.dataset import Dataset
from ..perturbation.adv_region import AdversarialRegion
from ..space.distance import Closer


logger = logging.getLogger(__name__)

from src.utils.base_types import NDVector

VertexId = str

@dataclass
class Vertex:
  id: VertexId
  point: Optional[NDVector] = field(default=None)
  label: int = field(default=-1)
  closer_vertices: set[VertexId] = field(default_factory=set)
  edges: list[VertexId] = field(default_factory=list)
@dataclass
class AbstractVertex:
  id: str
  setv: frozenset[VertexId] = field(default_factory=frozenset)
  reqv: frozenset[VertexId] = field(default_factory=frozenset)
  predv: frozenset[VertexId] = field(default_factory=frozenset)
  len: int = field(default_factory=int)
  repr: str = field(default_factory=str)
  initialized: bool = field(init=False, default=False)
  sorted_setv: list[VertexId] = field(init=False, default_factory=list)

  def __post_init__(self: Self) -> None:
    self.initialized = True
    self.sorted_setv = sorted(self.setv)
    self.repr = self._encode()

  def __setattr__(self, prop: Any, val: Any):
    super().__setattr__(prop, val)
    if self.initialized  and prop in ["reqv", "len"]:
        self.repr = self._encode()

  def labels(self: Self, graph: DominanceGraph) -> list[Counter[int]]:
    label_bags: list[Counter[int]] = []

    req_labels = Counter([graph[v].label for v in self.reqv])
    remaining_vertices = self.setv - self.reqv

    if len(remaining_vertices) == 0:
      return  [req_labels]

    remaining_labels = [graph[v].label for v in remaining_vertices]
    for labels in combinations(remaining_labels, self.len - len(self.reqv)):
      label_bags.append(req_labels + Counter(labels))

    return label_bags

  def _encode(self: Self) -> str:
    return  (
      "{" +
      ",".join([id if id not in self.reqv else f'[{id}]' for id in self.sorted_setv]) +
      "}-" + str(self.len)
    )

  def __str__(self) -> str:
    return self.repr

@dataclass(eq=False)
class AbstractPath:
  abs_vertices: dict[str, AbstractVertex] = field(default_factory=dict)
  length: int = field(default_factory=int)

  @cached_property
  def setp(self: Self) -> set[VertexId]:
    return reduce(frozenset.union, [av.setv for av in self.abs_vertices.values()], # type: ignore
                   frozenset()) # type: ignore

  def is_safe(self: Self, abs_vertex: AbstractVertex) -> bool:

    if abs_vertex.id in self.abs_vertices:
      existing_vertex = self.abs_vertices[abs_vertex.id]
      return abs_vertex.len + existing_vertex.len <= len(existing_vertex.setv)

    if not abs_vertex.predv <= self.setp:
      return False

    for a_vertex in self.abs_vertices.values():
      if len((abs_vertex.predv | a_vertex.reqv) & a_vertex.setv) > a_vertex.len:
        return False

    return True

  def extend(self: Self, abs_vertex: AbstractVertex) -> AbstractPath:
    new_abs_vertices = deepcopy(self.abs_vertices)
    # new_abs_vertices: dict[str, AbstractVertex] = {}

    if abs_vertex.id in new_abs_vertices:
      new_abs_vertices[abs_vertex.id].len += abs_vertex.len
    else:
      for id in new_abs_vertices:
        new_abs_vertices[id].reqv |=  (abs_vertex.predv & new_abs_vertices[id].setv)

      new_abs_vertices[abs_vertex.id] = abs_vertex

    return AbstractPath(
      new_abs_vertices,
      length = self.length + abs_vertex.len
    )

  def labels_star(self: Self, graph: DominanceGraph) -> list[Counter[int]]:
    label_bags: list[Counter[int]] = []

    for counters in product(*[av.labels(graph) for av in self.abs_vertices.values()]):
      empty: Counter[int] = Counter()
      label_bags.append(sum(counters, empty))

    return label_bags

  def __eq__(self, other: object) -> bool:

    if isinstance(other, AbstractPath):
      return self.repr == other.repr

    return False

  @cached_property
  def repr(self: Self) -> set[str]:
    return set([str(av) for av in self.abs_vertices.values()])

  def __repr__(self: Self) -> str:
    return ", ".join([str(av) for av in self.abs_vertices.values()])

  @classmethod
  def emptyPath(cls:  type[AbstractPath]) -> AbstractPath:
    return cls()

@dataclass
class DominanceGraph:
  vertices: dict[VertexId, Vertex]

  def __getitem__(self: Self, key: VertexId) -> Vertex:
    return self.vertices[key]

  def get_neighbours_label(self: Self, k_vals: list[int]) -> dict[int, set[int]]:

    def build_abs_vertices(min_length: int, vertices: Iterable[Vertex]) -> list[AbstractVertex]:

      abs_vertices: list[AbstractVertex] = []
      underlying_sets: defaultdict[str, list[Vertex]] = defaultdict(list)

      for vertex in vertices:
        abs_vertex_id = f'{min_length}-{hash(frozenset(vertex.closer_vertices))}'
        underlying_sets[abs_vertex_id].append(vertex)

      for id, u_set in  underlying_sets.items():
        abs_vertices.append(
          AbstractVertex(
            id=id,
            setv=frozenset(sorted([v.id for v in u_set])),
            reqv=frozenset(),
            predv=frozenset(u_set[0].closer_vertices),
            len=1
          )
        )

      return abs_vertices

    def get_possible_classifications(abs_paths: list[AbstractPath], graph: DominanceGraph) -> set[int]:
      classifications: set[int] = set()

      for abs_path in abs_paths:
        for label_counter in abs_path.labels_star(graph):

          max_freq: int = label_counter.most_common(1)[0][1]
          most_freq_labels: list[int] = [label for label,v in label_counter.items() if v == max_freq]

          classifications.update(most_freq_labels)

      return classifications

    def extend_abs_paths(abs_paths: list[AbstractPath],
                         abs_vertices: list[AbstractVertex])  -> list[AbstractPath]:

      new_paths: list[AbstractPath] = []
      for abs_vertex in abs_vertices:
        for abs_path in abs_paths:

          if abs_path.is_safe(abs_vertex):
            new_path = abs_path.extend(abs_vertex)

            if new_path not in new_paths:
              new_paths.append(new_path)

      return new_paths

    max_k = max(k_vals)

    abs_paths: defaultdict[int, list[AbstractPath]] = defaultdict(list)
    abs_paths[0] = [AbstractPath.emptyPath()]
    abs_vertices: list[AbstractVertex] = []

    result:  dict[int, set[int]] = defaultdict(set)

    graph_vertices: list[Vertex] = [v for id,v in self.vertices.items() if id != 'root' ]
    graph_vertices = sorted(graph_vertices, key=lambda val: len(val.closer_vertices))
    graph_vertices = [v for v in graph_vertices if len(v.closer_vertices) < max_k]

    k: int = 1
    for min_length, vertices in groupby(graph_vertices, lambda val: len(val.closer_vertices)):

      if k > max_k:
        break

      while k-1 < min_length :
        abs_paths[k] = extend_abs_paths(abs_paths[k-1], abs_vertices)
        result[k] = get_possible_classifications(abs_paths[k], self)
        k += 1

      abs_vertices.extend(build_abs_vertices(min_length, vertices))

      abs_paths[k] = extend_abs_paths(abs_paths[k-1], abs_vertices)
      result[k] = get_possible_classifications(abs_paths[k], self)
      k += 1

    while k-1 <= max_k:
      abs_paths[k]= extend_abs_paths(abs_paths[k-1], abs_vertices)
      result[k] = get_possible_classifications(abs_paths[k], self)
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