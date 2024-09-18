from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from heapq import heapify, heappop, heappush
from typing import Optional, Self, Type
from  pprint import pformat
from textwrap import indent
import logging
from itertools import repeat

from ..perturbation.perturbation import AdvRegion
from ..space.hyperplane import Hyperplane
from ..space.polyhedron import Polyhedron

from ..dataset.dataset import Dataset
from ..space.distance import Closer

logger = logging.getLogger(__name__)

from src.utils.base_types import  Array1xN, NDVector

VertexId = str
Label = int

@dataclass
class Vertex:
  id: VertexId
  point: Optional[NDVector] = field(default=None)
  label: int = field(default=-1)
  closer_vertices: set[VertexId] = field(default_factory=set)
  equidistant_vertices: set[VertexId] = field(default_factory=set)
  edges: list[VertexId] = field(default_factory=list)

@dataclass(order=True)
class PrioritizedItem:
    priority: tuple[int, int]
    item: ConcretePath=field(compare=False)

class Safe_Vertex_Error(Enum):
  MISSING_ANCESTOR = auto()
  CIRCULAR_PATH    = auto()
  UNSATISFIED_LP   = auto()
  NONE             = auto()

@dataclass
class ConcretePath:
  vertices: list[VertexId] = field(default_factory=list)
  polyhedron: Polyhedron = field(default_factory=Polyhedron.dummyPolyhedron)
  label_counter: Counter[int] = field(default_factory=Counter)

  @property
  def last(self: Self) -> VertexId:
    return self.vertices[-1]

  @property
  def most_common_label(self: Self) -> tuple[int, int]:
    return self.label_counter.most_common(1)[0]

  def len(self: Self) -> int:
    return len(self.vertices)

  def is_safe(self: Self, vertex: Vertex,
              bisectors: dict[tuple[VertexId, VertexId], Hyperplane],
              dom_graph : DominanceGraph) -> tuple[Safe_Vertex_Error, None | Polyhedron]:

    def build_new_polyhedrons() -> Polyhedron:
      not_ancestor = set(self.vertices) - vertex.closer_vertices

      inequalities_lhs: list[Array1xN] = []
      inequalities_rhs: list[float] = []

      equidistant_vertices: set[VertexId] = \
            vertex.equidistant_vertices - set(self.vertices)

      equidistant_vertices = set(
        [v_id for v_id in equidistant_vertices
         if len(dom_graph[v_id].closer_vertices) <= self.len()
        ]
      )

      if not not_ancestor and not equidistant_vertices:
        return self.polyhedron.copy()

      if equidistant_vertices:
        for v in equidistant_vertices:
          if (vertex.id, v) in bisectors:
            bisector = bisectors[(vertex.id, v)]
            inequalities_lhs.append(bisector.coefficients)
            inequalities_rhs.append(bisector.constant)
          else:
            bisector = bisectors[(v, vertex.id)]
            inequalities_lhs.append(-bisector.coefficients)
            inequalities_rhs.append(-bisector.constant)

      if not_ancestor:
        for v in not_ancestor:
          if (v, vertex.id) in bisectors:
            bisector = bisectors[(v, vertex.id)]
            inequalities_lhs.append(bisector.coefficients)
            inequalities_rhs.append(bisector.constant)
          else:
            bisector = bisectors[(vertex.id, v)]
            inequalities_lhs.append(-bisector.coefficients)
            inequalities_rhs.append(-bisector.constant)

      return self.polyhedron.refine(inequalities_lhs, inequalities_rhs) # type: ignore

    missing_ancestor: bool = bool(vertex.closer_vertices) and \
                                  (not vertex.closer_vertices <= set(self.vertices))
    circular_path: bool = vertex.id in self.vertices

    if missing_ancestor:
      return Safe_Vertex_Error.MISSING_ANCESTOR, None

    if circular_path:
      return Safe_Vertex_Error.CIRCULAR_PATH, None

    new_polyhedron = build_new_polyhedrons()

    if not new_polyhedron.is_valid():
      return Safe_Vertex_Error.UNSATISFIED_LP, None

    return Safe_Vertex_Error.NONE, new_polyhedron

  def add_vertex(self: Self, vertex: Vertex,
                  bisectors: dict[tuple[VertexId, VertexId], Hyperplane],
                  dom_graph : DominanceGraph)  -> Safe_Vertex_Error | ConcretePath:

    safe_error, polyhedron = self.is_safe(vertex, bisectors, dom_graph)

    if safe_error != Safe_Vertex_Error.NONE:
      return safe_error

    assert polyhedron is not None
    return ConcretePath(
      self.vertices + [vertex.id],
      polyhedron,
      self.label_counter + Counter([vertex.label])
    )

  def __len__(self: Self) -> int:
    return len(self.vertices)

  def __eq__(self: Self, other: object) -> bool:

    if not isinstance(other, ConcretePath):
      return False

    return self.vertices == other.vertices

  def __str__(self) -> str:
    return '[' + ', '.join(self.vertices) + ']'


  @classmethod
  def emptyPath(cls:  type[ConcretePath]) -> ConcretePath:
    return cls()
  @classmethod
  def singlePath(cls:  type[ConcretePath], vertexId: VertexId) -> ConcretePath:
    return cls([vertexId])

  @classmethod
  def check_path(cls: type[ConcretePath],
                 init_path: ConcretePath,
                 vertices: list[VertexId],
                 bisectors: dict[tuple[VertexId, VertexId], Hyperplane],
                 dom_graph : DominanceGraph,
) -> list[bool]:

    curr_path: ConcretePath = init_path
    valid_lengths = list(repeat(False, len(vertices)))
    for ix, vx in enumerate(vertices):
      res = curr_path.add_vertex(dom_graph[vx], bisectors, dom_graph)

      if isinstance(res, ConcretePath):
        valid_lengths[ix] = True
        curr_path = res
      else:
        break

    return valid_lengths

@dataclass
class DominanceGraph:
  vertices: dict[VertexId, Vertex]

  bisectors: dict[tuple[VertexId, VertexId], Hyperplane]

  def __getitem__(self: Self, key: VertexId) -> Vertex:
    return self.vertices[key]

  def _get_label_occurrences(self: Self, max_k_value: int) -> dict[int, list[Vertex]]:

    labels_vertices: defaultdict[int, list[Vertex]] = defaultdict(list)

    label_count: Counter[int] = Counter([
      v.label for v in self.vertices.values()
        if len(v.closer_vertices) < max_k_value  and v.id != 'root'
    ])

    for vx in filter(lambda v: v.id != 'root', self.vertices.values()):

      lb_count = Counter([self[v].label for v in  vx.closer_vertices])
      another_label_majority = False
      if len(lb_count) > 0:
        most_common = lb_count.most_common(1)[0]
        another_label_majority = most_common[1] >= max_k_value//2 +1

      if another_label_majority:
        continue

      if label_count[vx.label] >= (len(vx.closer_vertices) + 1)//2:
        labels_vertices[vx.label].append(vx)

    return labels_vertices

  def get_neighbors_label(self: Self, k_vals: list[int], numPoint: int) -> dict[int, set[int]]:

    def calculate_max_path_length(vertices: list[Vertex], max_length: int,
                                  labels_count: dict[int, list[Vertex]] ) -> int:

      current_path: set[VertexId] = set()
      vertex_added: int = 0

      for vx in [v for v in vertices if v.id not in current_path]:

        if not current_path >= vx.closer_vertices:
          current_path |= vx.closer_vertices

        if len(current_path) >= max_length:
          break

        current_path.add(vx.id)
        vertex_added += 1

      return min(sum([
              min(vertex_added, len(vxs)) for vxs in labels_count.values()
            ]), max_length)

    def extend_path(path: ConcretePath, vertex: Vertex,
                    queue: list[PrioritizedItem],
                    distinct_paths: defaultdict[int, set[tuple[VertexId,...]]],
                    len_priority: int = 1) -> bool:

      path_length: int = len(path)
      if tuple(path.vertices + [vertex.id]) not in distinct_paths[path_length+1]:

        result = path.add_vertex(vertex, self.bisectors, self)

        if isinstance(result, ConcretePath):
          item: PrioritizedItem = PrioritizedItem(
            (-result.label_counter[label], len_priority*result.len()),
            result
          )
          heappush(queue, item)
          current_distinct_paths[path_length+1].add(tuple(result.vertices))
          return True

        if result == Safe_Vertex_Error.MISSING_ANCESTOR:
          for ancestor in vertex.closer_vertices - set(path.vertices):
            extend_path(path, self[ancestor], queue, distinct_paths, len_priority)
          return True

      return False

    def skip_vertex(path: ConcretePath, vertex: Vertex, label_count: int,
                    max_path_length: int) -> bool:

      potential_path = set(path.vertices) | vertex.closer_vertices

      if len(potential_path) >= max_path_length:
        return True

      lb_count = Counter([self[v].label for v in potential_path])
      lb_count.update([vertex.label])
      most_common = lb_count.most_common(1)[0]

      insufficient_vertex: bool  = most_common[1] - lb_count[label] > \
                            label_count - lb_count[label]

      insufficient_length = most_common[1] - lb_count[label] >\
                            max_path_length - (len(potential_path)+1)


      if insufficient_vertex or insufficient_length:
        return True

      return False

    def get_initial_paths(label_vertices: list[Vertex],
                          labels_vertices: dict[int, list[Vertex]],
                          k_classified_with: dict[int, list[bool]],
                          classifications: dict[int, set[int]],
                          current_distinct_paths: defaultdict[int, set[tuple[VertexId,...]]],
                          max_k: int) -> list[ConcretePath]:

      init_paths: list[ConcretePath] = []

      priority_queue: list[PrioritizedItem] = []
      heappush(priority_queue, PrioritizedItem((0, 0), ConcretePath.emptyPath()))

      label_count = len(label_vertices)
      max_path_length = calculate_max_path_length(label_vertices, max_k, labels_vertices)
      min_path_length = min([len(v.closer_vertices) for v in label_vertices])

      k_classified_with[label][:min_path_length] = list(repeat(True, min_path_length))
      for ix in [i for i in range(max_k) if i+1 not in k_vals]:
        k_classified_with[label][ix] = True

      while len(priority_queue):

        path: ConcretePath = heappop(priority_queue).item
        path_length: int = len(path)

        if all(k_classified_with[label][path_length-1:]):
          continue

        if path_length >= max_k//2 + 1:
          most_commons = path.label_counter.most_common(2)

          if len(most_commons) == 1 or \
            most_commons[0][1] - most_commons[1][1] > max_k - path_length:

            for k in range(path_length, max_k+1):

              if k in k_vals:
                classifications[k].add(most_commons[0][0])
                k_classified_with[most_commons[0][0]][k-1] = True

            if most_commons[0][0] == label:
              k_with_missing_label: list[int] = [ix for ix, val in enumerate(k_classified_with[label])
                                                    if not val]
              max_path_length = 0 if not k_with_missing_label else k_with_missing_label[0] + 1
              priority_queue = [item for item in priority_queue
                                      if abs(item.priority[1]) < max_path_length]
              heapify(priority_queue)

            continue

        if path_length > 0:
          max_freq: int = path.label_counter.most_common(1)[0][1] # type: ignore
          most_freq_labels: list[int] = [k for k,c in path.label_counter.items()\
                                          if c == max_freq]
          if path_length in k_vals:
            classifications[path_length] |= set(most_freq_labels)

          if label in most_freq_labels:
            k_classified_with[label][path_length-1] = True

            if path_length == max_path_length:
              k_with_missing_label: list[int] = [ix for ix, val in enumerate(k_classified_with[label])
                                                    if not val]
              max_path_length = 0 if not k_with_missing_label else k_with_missing_label[0] + 1
              priority_queue = [item for item in priority_queue
                                      if abs(item.priority[1]) < max_path_length]
              heapify(priority_queue)

          if all(k_classified_with[label][:max_path_length]):
            break

        continue_search: bool = False
        if path_length < max_path_length:

          for vertex in filter(lambda v: v.id not in path.vertices, label_vertices):

            if not skip_vertex(path, vertex, label_count, max_path_length):
              continue_search |= extend_path(path, vertex, priority_queue,
                                             current_distinct_paths, -1)

        if not continue_search and 0 < path_length < max_path_length\
           and path.most_common_label[1] <= path.label_counter[label]\
           and path not in init_paths:

            init_paths.append(path)

      return init_paths

    max_k: int = max(k_vals)
    classifications: dict[int, set[int]] = defaultdict(set)

    labels_vertices: dict[int, list[Vertex]] = self._get_label_occurrences(max_k)

    if len(labels_vertices) == 1:

      for k in k_vals:
        classifications[k].add(self.vertices['0'].label)

      return classifications

    vertices: list[Vertex] = [
      v for id,v in self.vertices.items() if id != 'root' and
                                             len(v.closer_vertices) < max_k
    ]

    vertices = sorted(vertices, key=lambda val: len(val.closer_vertices))

    k_classified_with: dict[int, list[bool]] = dict([
      (label, list(repeat(False, max_k))) for label in labels_vertices.keys()
    ])

    for label_vertices in labels_vertices.values():
      label:int = label_vertices[0].label
      current_distinct_paths: defaultdict[int, set[tuple[VertexId,...]]] = defaultdict(set)

      priority_queue: list[PrioritizedItem] = []
      heappush(priority_queue, PrioritizedItem((0, 0), ConcretePath.emptyPath()))

      label_count = len(label_vertices)
      max_path_length = calculate_max_path_length(label_vertices, max_k, labels_vertices)

      init_paths = get_initial_paths(label_vertices, labels_vertices,
                                     k_classified_with, classifications,
                                      current_distinct_paths, max_k)

      if all(k_classified_with[label]):
        continue

      for init_path in init_paths:
        possible_vertices: list[Vertex] = list(filter(
          lambda v: v.id not in init_path.vertices and not skip_vertex(init_path, v, label_count, max_path_length),
          vertices))

        possible_labels: set[Label] = set([v.label for v in possible_vertices])
        max_path_length = min(sum([
              min(init_path.label_counter[label], len(label_vertices))
                                                   for label in possible_labels
            ]), max_k)

        priority_queue: list[PrioritizedItem] = []
        heappush(
          priority_queue,
          PrioritizedItem((-init_path.label_counter[label], -len(init_path)), init_path)
        )

        while len(priority_queue):

          path: ConcretePath = heappop(priority_queue).item
          path_length: int = len(path)


          if not k_classified_with[label][path_length-1]:

            if path_length >= max_k//2 + 1:
              most_commons = path.label_counter.most_common(2)

              if len(most_commons) == 1 or \
                most_commons[0][1] - most_commons[1][1] > max_k - path_length:

                for k in range(path_length, max_k+1):

                  if k in k_vals:
                    classifications[k].add(most_commons[0][0])
                    k_classified_with[most_commons[0][0]][k-1] = True

                if most_commons[0][0] == label:
                  k_with_missing_label: list[int] = [ix for ix, val in enumerate(k_classified_with[label])
                                                        if not val]
                  max_path_length = 0 if not k_with_missing_label else k_with_missing_label[0] + 1
                  priority_queue = [item for item in priority_queue
                                          if abs(item.priority[1]) < max_path_length]
                  heapify(priority_queue)

                continue


            max_freq: int = path.label_counter.most_common(1)[0][1] # type: ignore
            most_freq_labels: list[int] = [k for k,c in path.label_counter.items()\
                                            if c == max_freq]
            if path_length in k_vals:
              classifications[path_length] |= set(most_freq_labels)

            if label in most_freq_labels:
              k_classified_with[label][path_length-1] = True

              if path_length == max_path_length:
                k_with_missing_label: list[int] = [ix for ix, val in enumerate(k_classified_with[label])
                                                      if not val]
                max_path_length = 0 if not k_with_missing_label else k_with_missing_label[0] + 1
                priority_queue = [item for item in priority_queue
                                        if abs(item.priority[1]) < max_path_length]
                heapify(priority_queue)

          if all(k_classified_with[label][:max_path_length]):
            break


          if path.most_common_label[1] <= path.label_counter[label]\
           and not all(k_classified_with[label][path_length-1:]):
            for adj in possible_vertices:
              if path.label_counter[label] >= path.label_counter[adj.label] + 1:
                extend_path(path, adj, priority_queue,current_distinct_paths, -1)


      # while len(priority_queue):

      #   path: ConcretePath = heappop(priority_queue).item
      #   # print(f'curr path: {path}', end='\r', flush=True)
      #   path_length: int = len(path)

      #   if all(k_classified_with[label][path_length-1:]):
      #     continue

      #   if not k_classified_with[label][path_length-1]:

      #     if path_length >= max_k//2 + 1:
      #       most_commons = path.label_counter.most_common(2)

      #       if len(most_commons) == 1 or \
      #         most_commons[0][1] - most_commons[1][1] > max_k - path_length:

      #         for k in range(path_length, max_k+1):

      #           if k in k_vals:
      #             classifications[k].add(most_commons[0][0])
      #             k_classified_with[most_commons[0][0]][k-1] = True

      #         if most_commons[0][0] == label:
      #           k_with_missing_label: list[int] = [ix for ix, val in enumerate(k_classified_with[label])
      #                                                 if not val]
      #           max_path_length = 0 if not k_with_missing_label else k_with_missing_label[0] + 1
      #           priority_queue = [item for item in priority_queue
      #                                   if abs(item.priority[1]) < max_path_length]
      #           heapify(priority_queue)

      #         continue

      #     if path_length > 0:
      #       max_freq: int = path.label_counter.most_common(1)[0][1] # type: ignore
      #       most_freq_labels: list[int] = [k for k,c in path.label_counter.items()\
      #                                       if c == max_freq]
      #       if path_length in k_vals:
      #         classifications[path_length] |= set(most_freq_labels)

      #       if label in most_freq_labels:
      #         k_classified_with[label][path_length-1] = True

      #         if path_length == max_path_length:
      #           k_with_missing_label: list[int] = [ix for ix, val in enumerate(k_classified_with[label])
      #                                                 if not val]
      #           max_path_length = 0 if not k_with_missing_label else k_with_missing_label[0] + 1
      #           priority_queue = [item for item in priority_queue
      #                                   if abs(item.priority[1]) < max_path_length]
      #           heapify(priority_queue)

      #     if all(k_classified_with[label][:max_path_length]):
      #       break

      #   continue_search: bool = False
      #   if path_length < max_path_length:

      #     for vertex in filter(lambda v: v.id not in path.vertices, label_vertices):

      #       if not skip_vertex(path, vertex, label_count, max_path_length):
      #         continue_search |= extend_path(path, vertex, priority_queue,
      #                                        current_distinct_paths, -1)

      #   if not continue_search and 0 < path_length < max_path_length\
      #      and path.most_common_label[1] <= path.label_counter[label]\
      #      and not all(k_classified_with[label][path_length-1:]):

      #     for adj in [vx for vx in vertices if vx.id not in path.vertices]:
      #       if path.label_counter[label] >= path.label_counter[adj.label] + 1 and\
      #         not skip_vertex(path, adj, label_count, max_path_length):

      #         extend_path(path, adj, priority_queue,current_distinct_paths, -1)

    return classifications

  @classmethod
  def build_dominance_graph(cls: Type[DominanceGraph],
                            adv_region: AdvRegion,
                            dataset: Dataset,
                            max_path_length: int = 7) -> DominanceGraph:

    bisectors: dict[tuple[VertexId, VertexId], Hyperplane] = dict()
    dom_matrix: dict[VertexId, Vertex] = dict(
      [(str(i), Vertex(str(i), dataset.points[i],  dataset.labels[i]))
                                            for i in range(dataset.num_points)]
    )

    initial_vertices: set[int] = set(range(dataset.num_points))
    to_remove: set[str] = set()

    for i in range(dataset.num_points):

      if len(dom_matrix[str(i)].closer_vertices) >= max_path_length:
        initial_vertices.discard(i)
        to_remove.add(str(i))
        continue

      for j in range(i+1, dataset.num_points):

        if len(dom_matrix[str(j)].closer_vertices) >= max_path_length:
          continue

        bisectors[(str(i), str(j))] = Hyperplane.build_equidistant_plane(
          dataset.points[i],
          dataset.points[j]
        )

        match adv_region.get_closer(bisectors[(str(i), str(j))]):

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
            dom_matrix[str(i)].equidistant_vertices.add(str(j))

            dom_matrix[str(j)].edges.append(str(i))
            dom_matrix[str(j)].equidistant_vertices.add(str(i))

    root_edges: list[VertexId]= [str(i) for i in initial_vertices]
    dom_matrix['root'] = Vertex('root', edges=root_edges)

    for node in to_remove:
      del dom_matrix[node]

    for vertex in dom_matrix.values():
      vertex.closer_vertices -= to_remove
      vertex.equidistant_vertices -= to_remove
      vertex.edges = [edge for edge in vertex.edges if edge not in to_remove]

    logger.debug("\t dominance graph: \n")
    logger.debug('%s\n', indent(pformat(dom_matrix, compact=True),'\t\t'))
    return cls(dom_matrix, bisectors)