from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from functools import total_ordering
from typing import Self
import heapq

@total_ordering
@dataclass(order=False)
class PriorityItem:
  val: int
  priority: float
  delta: list[float]

  def real_priority(self: Self) -> float:
    return abs(self.priority + self.delta[0])

  def __lt__(self: Self, __other: PriorityItem) -> bool:
    return self.real_priority() < __other.real_priority()

  def __eq__(self: Self, __other: object) -> bool:
    if not isinstance(__other, PriorityItem):
      return NotImplemented

    return self.real_priority() == __other.real_priority()

@dataclass
class PriorityQueue:
  data: InitVar[list[tuple[int, float]]]
  delta: list[float] = field(default_factory=list)
  size: int = field(init=False, default_factory=int)
  _data: list[PriorityItem]  = field(init=False)

  def __post_init__(self: Self, data: list[tuple[int, float]]) -> None:

    if len(self.delta) > 1:
      raise ValueError("Delta value con be only a single element list.")

    if not self.delta:
      self.delta = [0]

    if data:
      self._data = [PriorityItem(val, priority, self.delta) for val, priority in data]
      self.size = len(self._data)
      heapq.heapify(self._data)
    else:
      self._data = []
      self.size = 0


  def push(self: Self, val: int, priority: float, delta: list[float]) -> None:
    heapq.heappush(self._data, PriorityItem(val, priority, delta))
    self.size += 1

  def pop(self: Self) -> PriorityItem:
    item = heapq.heappop(self._data)
    self.size -= 1
    return item

  def peek(self: Self) -> PriorityItem:
    return self._data[0]

  def pushpop(self: Self, val: int, priority: float, delta: list[float]) -> PriorityItem:
    return heapq.heappushpop(self._data, PriorityItem(val, priority, delta))

  def incr_delta(self: Self, incr: float) -> None:
    self.delta[0] += incr

  def decr_delta(self: Self, decr: float) -> None:
    self.delta[0] -= decr

  def vals(self: Self) -> list[int]:
    return [item.val for item in self._data]

  def items(self: Self) -> list[tuple[int, float]]:
    return [(item.val, item.real_priority()) for item in self._data]