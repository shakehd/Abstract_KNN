
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Self

from typings.base_types import ArrayNxM, Integer, NDVector


@dataclass
class Dataset:
  points: ArrayNxM
  labels: NDVector

  num_points: Integer = field(init=False)

  def __post_init__(self: Self) -> None:
    self.num_points = self.points.shape[0]

  def __getitem__(self: Self, key: Any) -> Dataset:
    return Dataset(self.points[key], self.labels[key])