from collections import deque
from math import isclose
from typing import Callable, Deque, Iterable, TypeVar
from numpy import float_, sign
from sklearn.metrics import DistanceMetric

from ..utils.tree import Ball, Leaf, Node
from src.utils.base_types import NDVector
from src.space.distance import Closer, get_closer_manhattan, which_is_closer

def query_point(tree: Node | Leaf, point: NDVector, distance: DistanceMetric) -> list[Leaf]:

  return _query_space(deque([tree]), point, get_closer_from_point, distance)

def query_radius(tree: Node | Leaf, point: NDVector, radius: float, distance: DistanceMetric) -> list[Leaf]:

  return _query_space(deque([tree]), Ball(point, radius), get_closer_from_ball, distance)


TInp = TypeVar("TInp", bound= NDVector | Ball)

def _query_space(queue: deque[Node | Leaf], input: TInp,
                 get_closer: Callable[[TInp, Node, DistanceMetric], list[Node | Leaf]],
                 distance_metric: DistanceMetric) -> list[Leaf]:

  partitions: list[Leaf] = []

  while True:
    try:
      cur_node: Node | Leaf = queue.popleft()

      if isinstance(cur_node, Leaf):
        partitions.append(cur_node)

      else:

        next_nodes = get_closer(input, cur_node, distance_metric)
        queue.extend(next_nodes)

    except IndexError:
      break

  return partitions


def get_closer_from_point(point: NDVector, node: Node, distance_metric: DistanceMetric) -> list[Node | Leaf]:

  match which_is_closer(point,
                        node.left_child.ref_point,
                        node.right_child.ref_point, distance_metric):

    case Closer.BOTH:
      result = [node.left_child, node.right_child]

    case Closer.SECOND:
     result = [node.right_child]

    case Closer.FIRST:
      result = [node.left_child]

  return result

def get_closer_from_ball(ball: Ball, node: Node, distance_metric: DistanceMetric) -> list[Node | Leaf]:

  left_part_dist = distance_metric.pairwise([node.left_child.ref_point], [ball.center])[0]
  right_part_dist = distance_metric.pairwise([node.left_child.ref_point], [ball.center])[0]

  if isclose(left_part_dist, right_part_dist):
    return [node.left_child, node.right_child]

  if 'EuclideanDistance' in type(distance_metric).__name__:

    plane_dist = node.axial_hyperplane.distance_to_point(ball.center, distance_metric)
    if plane_dist <= ball.radius or isclose(plane_dist, ball.radius):
      return [node.left_child, node.right_child]
    if left_part_dist > right_part_dist:
      return [node.right_child]
    else:
      return [node.left_child]

  elif 'Manhattan' in type(distance_metric).__name__:

    match get_closer_manhattan(ball.center, node.left_child.ref_point,
                             node.left_child.ref_point, 2*ball.radius,
                             ball.radius, distance_metric, ball.radius):

      case Closer.BOTH:
        result = [node.left_child, node.right_child]

      case Closer.SECOND:
        result =  [node.right_child]

      case Closer.FIRST:
        result =  [node.left_child]

    return result

  else:
    raise ValueError(f'distance metric {type(distance_metric).__name__} not supported')
