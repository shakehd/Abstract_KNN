
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable, Self
from numpy import vstack, hstack

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

  @classmethod
  def vstack(cls: type[Dataset], *datasets: Dataset) -> Dataset:
    points: list[ArrayNxM] = [d.points for d in datasets]
    labels: list[ArrayNxM] = [d.labels for d in datasets]

    return cls(vstack(points), hstack(labels))