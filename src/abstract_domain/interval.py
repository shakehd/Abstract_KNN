from dataclasses import dataclass, field
from typings.base_types import Real


@dataclass
class AbstractDomain:
  lb: Real = field(init=False, default=0.0)
  ub: Real = field(init=False, default=0.0)