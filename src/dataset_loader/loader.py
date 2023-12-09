
from dataclasses import dataclass
from typing import Any, Mapping, Self
from .dataset import Dataset

from typings.base_types import String


@dataclass
class DataLoader:
  params: Mapping[String, Any]

  def load_datasets(self: Self) -> tuple[Dataset, Dataset]:
    pass
