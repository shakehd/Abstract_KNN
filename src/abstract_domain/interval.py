from dataclasses import dataclass, field
from typing import Self
from typings.base_types import Real, String
from numpy import inf


@dataclass
class Interval:
  lb: float = field(default=float('-inf'))
  ub: float = field(default=float('inf'))

  def __str__(self: Self) -> String:
    return f'[{self.lb}, {self.ub}]'