from math import isclose
from typing import Callable, Deque, Iterable, TypeVar
from .random_ball_tree import Leaf, Node
from typings.base_types import Array1xM
from ..utils.ndball import NDBall
from src.utils.distance import Selection, squared_dist, which_is_closer

T = TypeVar("T", bound= Array1xM | NDBall)

def search_partitions(queue: Deque[Node | Leaf], point: T,
                      find_closest_child: Callable[[T, Node], Iterable[Node | Leaf]]) -> list[Leaf]:

  partitions: list[Leaf] = []

  while True:
    try:
      cur_node: Node | Leaf = queue.popleft()

      if isinstance(cur_node, Leaf):
        partitions.append(cur_node)

      else:
        next_nodes = find_closest_child(point, cur_node)
        queue.extend(next_nodes)

    except IndexError:
      break

  return partitions


def find_closest_child_from_point(point: Array1xM, node: Node) -> Iterable[Node | Leaf]:

  match which_is_closer(point, node.left_child.ref_point, node.right_child.ref_point):

    case Selection.BOTH:
      result = [node.left_child, node.right_child]

    case Selection.SECOND:
      result = [node.right_child]

    case Selection.FIRST:
      result = [node.left_child]

  return result

def find_closest_from_ball(ball: NDBall, node: Node) -> Iterable[Node | Leaf]:
  left_dist = squared_dist(node.left_child.ref_point, ball.center)
  right_dist = squared_dist(node.left_child.ref_point, ball.center)

  if isclose(left_dist, right_dist):
    return [node.left_child, node.right_child]
  else:
    plane_dist = node.axial_hyperplane.distance_to_point(ball.center)**2
    if plane_dist <= ball.radius:
       return [node.left_child, node.right_child]
    if left_dist > right_dist:
      return [node.right_child]
    else:
      return [node.left_child]