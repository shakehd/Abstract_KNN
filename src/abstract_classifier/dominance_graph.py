from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from typing import  Optional, Self, Type
from .. dataset_loader.dataset import Dataset
from .. perturbation.adv_region import AdversarialRegion
from .. utils.distance import Selection, which_is_closer

from typings.base_types import Integer, NDVector, Number, String

Id = String

@dataclass
class Vertex:
  id: Id
  label: int = field(default=-1)
  edges: list[Id] = field(default_factory=list)
  required_ancestors: set[Id] = field(default_factory=set)


@dataclass
class DominanceGraph:
  vertices: dict[Id, Vertex]

  def __getitem__(self: Self, key: Id) -> Vertex:
    return self.vertices[key]


  def get_neighbors(self: Self, k: Number) -> list[list[Number]]:

    queue: deque[list[Id]] = deque([[v] for v in self['root'].edges])
    possible_labels: list[list[Number]] = []

    while True:
      try:
        neighbors: list[Id] = queue.popleft()

        if len(neighbors) > k:
          continue

        if len(neighbors) == k:

          possible_labels.append([self[id].label for id in neighbors])

        else:
          sneighbors: set[Id] = set(neighbors)
          frontier_vertex_id: Id = neighbors[-1]

          for adj_id in self[frontier_vertex_id].edges:
            missing_ancestor: bool = bool(self[adj_id].required_ancestors & sneighbors)
            circular_path: bool = adj_id == frontier_vertex_id

            if not missing_ancestor and not circular_path:
              queue.append(neighbors + [adj_id])
      except IndexError:
        break

    return possible_labels


  @classmethod
  def build_dominance_graph(cls: Type[DominanceGraph], adv_region: AdversarialRegion,
                            dataset: Dataset) -> DominanceGraph:

    def closer_to_adv_region(fst_point: NDVector, snd_point: NDVector) -> Selection:

      match which_is_closer(adv_region.point, fst_point, snd_point):

        case Selection.BOTH:
          return Selection.BOTH

        case Selection.FIRST:
          target_point = adv_region.perturbation_closest_point(snd_point)

        case Selection.SECOND:
          target_point = adv_region.perturbation_closest_point(fst_point)

      return which_is_closer(target_point, fst_point, snd_point)


    dom_matrix: dict[String, Vertex] = dict(
      *[(str(i), Vertex(str(i), dataset.labels[i])) for i in range(dataset.num_points)]
    )
    initial_vertices: set[Integer] = set(range(dataset.num_points))

    for i in range(dataset.num_points):
      for j in range(i + 1, dataset.num_points):
        match closer_to_adv_region(dataset.points[i], dataset.points[j]):

          case Selection.FIRST:
            dom_matrix[str(i)].edges.append(str(j))
            dom_matrix[str(j)].required_ancestors.add(str(i))
            initial_vertices.remove(j)

          case Selection.SECOND:
            dom_matrix[str(j)].edges.append(str(i))
            dom_matrix[str(i)].required_ancestors.add(str(j))
            initial_vertices.remove(i)

          case Selection.BOTH:
            dom_matrix[str(i)].edges.append(str(j))
            dom_matrix[str(j)].edges.append(str(i))

    root_edges: list[String]= [str(i) for i in range(dataset.num_points)]
    dom_matrix['root'] = Vertex('root', edges=root_edges)

    return cls(dom_matrix)




