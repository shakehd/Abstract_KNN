from dataclasses import dataclass, field
from typing import Self
from base_types import Array1xM
import numpy as np


@dataclass
class NDBall:
  center: Array1xM = field()
  radius: np.float_ = field(default_factory=np.float_)

  def is_inside(self: Self, point: Array1xM) -> bool:

    if np.linalg.norm(self.center - point, ord=2)**2 <= self.radius**2:
      return True

    return False