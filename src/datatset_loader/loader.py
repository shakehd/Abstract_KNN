
from dataclasses import dataclass
from typing import Any, Mapping, Self, Tuple
from .dataset import Dataset

from typings.base_types import String


@dataclass
class DataLoader:
  params: Mapping[String, Any]

  def load_datasets(self: Self) -> Tuple[Dataset, Dataset]:
    pass
