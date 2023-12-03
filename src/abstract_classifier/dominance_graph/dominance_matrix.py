from dataclasses import dataclass, field
from enum import Enum

from base_types import ArrayNxN


class Position(Enum):
  CLOSER  = 1
  BOTH    = 0
  FURTHER = -1

@dataclass
class DominantMatrix:
  matrix: ArrayNxN = field()




