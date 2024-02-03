
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, NotRequired, Required, Self, TypedDict
from numpy import vstack, hstack

from typings.base_types import ArrayNxM, Integer, NDVector


class DatasetParams(TypedDict, total=False):
  format: Required[str]
  training_set: Required[str]
  test_set: Required[str]
  category_indexes: NotRequired[list[int]]


@dataclass
class Dataset:
  points: ArrayNxM
  labels: NDVector
  num_feature_start_ix: int

  num_points: Integer = field(init=False)


  def __post_init__(self: Self) -> None:
    self.num_points = self.points.shape[0]

  def __getitem__(self: Self, key: Any) -> Dataset:
    return Dataset(self.points[key], self.labels[key], self.num_feature_start_ix)

  @classmethod
  def vstack(cls: type[Dataset], *datasets: Dataset) -> Dataset:
    points: list[ArrayNxM] = [d.points for d in datasets]
    labels: list[ArrayNxM] = [d.labels for d in datasets]

    return cls(vstack(points), hstack(labels), datasets[0].num_feature_start_ix)