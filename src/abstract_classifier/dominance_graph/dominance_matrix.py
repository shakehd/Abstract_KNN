from dataclasses import dataclass, field
from enum import Enum
from typing import Type
import numpy as np

from typings.base_types import ArrayNxM, ArrayNxN


class Position(Enum):
  CLOSER  = 1
  BOTH    = 0
  FURTHER = -1

@dataclass
class DominantMatrix:
  matrix: ArrayNxN = field()




