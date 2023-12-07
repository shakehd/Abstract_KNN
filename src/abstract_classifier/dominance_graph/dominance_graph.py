from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import  Mapping, Optional, Sequence, Type
from src.perturbation.adv_region import AdversarialRegion

from typings.base_types import  ArrayNxM, NDVector, Number, String

class Position(Enum):
  CLOSER  = 1
  BOTH    = 0
  FURTHER = -1
@dataclass
class Vertex:
  id: String
  label: Optional[Number] = None

@dataclass
class Edge:
  orig: Vertex
  end: Vertex

  required_ancestors: list[String] = field(default_factory=list)

@dataclass
class DominanceGraph:
  vertices: Mapping[String, set[Vertex]]

  @classmethod
  def build_dominance_graph(cls: Type[DominanceGraph], adv_region: AdversarialRegion,
                            points: ArrayNxM) -> DominanceGraph:

    def relative_position(fst_point: NDVector, snd_point: NDVector) -> Position:
      return Position.BOTH

    num_points = points.shape[0]
    dom_matrix: defaultdict[String, set[Vertex]] = defaultdict(set)

    for i in range(num_points):
      for j in range(i + 1, num_points):
        match relative_position(points[i], points[j]):

          case Position.CLOSER: dom_matrix[str(i)].add(Vertex(str(j), ))





