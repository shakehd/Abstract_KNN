from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Self, Sequence
from scipy.optimize import linprog # type: ignore
import numpy as np

from src.utils.base_types import Array1xN, ArrayNxM

@dataclass
class Polyhedron:
  inequalities_lhs: ArrayNxM
  inequalities_rhs: Array1xN

  bounds: ClassVar[Sequence[tuple[float, float| None]]] = []
  equalities_lhs: ClassVar[ArrayNxM] = np.array([])
  equalities_rhs: ClassVar[Array1xN] = np.array([])

  def is_valid(self: Self) -> bool:

    if len(self.inequalities_lhs) == 0:
      return True

    solution = linprog(
      c=np.zeros(len(self.bounds)),
      A_ub = self.inequalities_lhs,
      b_ub = self.inequalities_rhs,
      A_eq = self.equalities_lhs,
      b_eq = self.equalities_rhs,
      bounds = self.bounds
    )

    return solution.success # type: ignore

  def refine(self: Self, inequality_lhs: ArrayNxM,
                     inequality_rhs: Array1xN) -> Polyhedron:
    new_inequalities_lhs = np.vstack((self.inequalities_lhs, inequality_lhs))
    new_inequalities_rhs = np.hstack((self.inequalities_rhs, inequality_rhs))

    return Polyhedron(new_inequalities_lhs, new_inequalities_rhs) # type: ignore

  def copy(self: Self) -> Polyhedron:
    return Polyhedron(
      self.inequalities_lhs.copy(),
      self.inequalities_rhs.copy()
    )

  @classmethod
  def dummyPolyhedron(cls:  type[Polyhedron]) -> Polyhedron:
    return cls(
      np.empty(shape=(0, len(Polyhedron.bounds))),
      np.array([])
    )
