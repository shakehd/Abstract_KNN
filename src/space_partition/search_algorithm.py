
from math import isclose
from typing import Callable, Deque, Iterable, List
from space_partition.random_ball_tree import Leaf, Node, TNode
from base_types import Array1xM
from utils.ndball import NDBall
from utils.utils import squared_dist

def search_partitions[TInput: Array1xM | NDBall](queue: Deque[TNode], point: TInput,
                       find_closest_child: Callable[[TInput, Node], Iterable[TNode]]) -> List[Leaf]:

  partitions: List[Leaf] = []

  while True:
    try:
      cur_node: TNode = queue.popleft()

      if isinstance(cur_node, Leaf):
        partitions.append(cur_node)

      else:
        next_nodes = find_closest_child(point, cur_node)
        queue.extend(next_nodes)

    except IndexError:
      break

  return partitions


def find_closest_child_from_point(point: Array1xM, node: Node) -> Iterable[TNode]:
  left_dist = squared_dist(node.left_child.ref_point, point)
  right_dist = squared_dist(node.right_child.ref_point, point)

  if isclose(left_dist, right_dist):
    return [node.left_child, node.right_child]
  else:
    if left_dist > right_dist:
      return [node.left_child]
    else:
      return [node.right_child]

def find_closest_from_ball(ball: NDBall, node: Node) -> Iterable[TNode]:
  left_dist = squared_dist(node.left_child.ref_point, ball.center)
  right_dist = squared_dist(node.left_child.ref_point, ball.center)

  if isclose(left_dist, right_dist):
    return [node.left_child, node.right_child]
  else:
    plane_dist = node.axial_hyperplane.distance_to_point(ball.center)**2
    if plane_dist <= ball.radius:
       return [node.left_child, node.right_child]
    if left_dist > right_dist:
      return [node.left_child]
    else:
      return [node.right_child]