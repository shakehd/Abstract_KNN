from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
from src.perturbations.perturbation import Perturbation

from typings.base_types import Array1xM, ArrayNxM, String

@dataclass
class Vertex:
  id: String
  point: Array1xM
  edges: Iterable['Edge'] = field(default_factory=list)

@dataclass
class Edge:
  orig: Vertex
  end: Vertex

  required_ancestors: Iterable[String] = field(default_factory=list)

@dataclass
class DominanceGraph:
  vertices: Iterable[Vertex]

