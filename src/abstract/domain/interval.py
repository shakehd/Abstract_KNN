from dataclasses import dataclass, field
from typing import Self


@dataclass
class Interval:
  lb: float = field(default=float('-inf'))
  ub: float = field(default=float('inf'))

  def __str__(self: Self) -> str:
    return f'[{self.lb}, {self.ub}]'