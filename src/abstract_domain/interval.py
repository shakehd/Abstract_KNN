from dataclasses import dataclass, field
from typing import Self
from typings.base_types import Real, String
import math


@dataclass
class Interval:
  lb: Real = field(default=-math.inf)
  ub: Real = field(default=math.inf)

  def __str__(self: Self) -> String:
    return f'[{self.lb}, {self.ub}]'