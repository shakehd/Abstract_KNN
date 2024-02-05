from dataclasses import dataclass
from math import isclose
from typing import Optional
from sklearn.metrics import DistanceMetric
import numpy as np
from sklearn.decomposition import PCA

from src.space.hyperplane import Hyperplane
from src.utils.priority_queue import PriorityItem, PriorityQueue
from typings.base_types import ArrayNxM, NDVector

@dataclass
class Cluster:
  left_indices: NDVector
  left_center: NDVector

  right_indices: NDVector
  right_center: NDVector


def two_means(dataset: ArrayNxM, indices: NDVector, distance_metric: DistanceMetric,
              random_state: Optional[int] = None) -> Cluster:

  left_center, right_center, points_idx = __get_initial_centers(dataset, indices, distance_metric, random_state)

  left_points_ids: PriorityQueue = PriorityQueue([])
  right_points_ids: PriorityQueue = PriorityQueue([])

  to_right = (right_center - left_center) / np.linalg.norm(right_center - left_center)
  to_left = (left_center - right_center) / np.linalg.norm(left_center - right_center)

  coefs: NDVector = 2*(left_center - right_center)

  const: float  = (left_center**2).sum() - (right_center**2).sum()

  initial_plane: Hyperplane = Hyperplane(coefs, const)

  for ix in points_idx:

    dist_centers = distance_metric.pairwise([dataset[ix]], [left_center, right_center])[0]
    dist: float = initial_plane.distance_to_point(dataset[ix], distance_metric)

    if initial_plane(dataset[ix]) >= 0:
      delta = left_points_ids.delta
    else:
      delta = right_points_ids.delta

    if isclose(*dist_centers) or dist_centers[0] <= dist_centers[1]:
      closer_cluster, further_cluster, dir = left_points_ids, right_points_ids, to_left

    else:
      closer_cluster, further_cluster, dir = right_points_ids, left_points_ids, to_right

    if closer_cluster.size <= further_cluster.size:

      closer_cluster.push(ix, dist, delta)

    else:

      old_edge_point: PriorityItem = closer_cluster.pushpop(ix, dist, delta)
      cur_edge_point: PriorityItem = closer_cluster.peek()

      new_delta: float = (old_edge_point.real_priority() + cur_edge_point.real_priority()) / 2

      left_center = left_center + dir*new_delta
      right_center = right_center + dir*new_delta

      closer_cluster.decr_delta(new_delta)
      further_cluster.incr_delta(new_delta)

      further_cluster.push(old_edge_point.val, old_edge_point.priority, delta)

  return Cluster(np.array(left_points_ids.vals()), left_center,
                 np.array(right_points_ids.vals()), right_center)


def __get_initial_centers(dataset: ArrayNxM, indices: NDVector,
                          distance_metric: DistanceMetric,
                          random_state: Optional[int]) -> tuple[NDVector, NDVector, NDVector]:

  if 'EuclideanDistance' in type(distance_metric).__name__:

    if random_state is not None:
      np.random.seed(random_state)

    point_idx: NDVector = np.random.permutation(indices)
    while np.allclose(dataset[point_idx[0]], dataset[point_idx[1]]):
      np.random.shuffle(point_idx)

    return dataset[point_idx[0]], dataset[point_idx[1]], point_idx

  if 'Manhattan' in type(distance_metric).__name__:

    pca = PCA(n_components=1, svd_solver='randomized')
    pca.fit(dataset)

    max_var_dim = np.argmax(pca.components_[0])

    max_vals = np.max(np.abs(dataset), axis=0)
    min_vals = np.min(np.abs(dataset), axis=0)

    left_center = np.array((max_vals + min_vals)/2)
    left_center[max_var_dim] = (6*min_vals[max_var_dim] + 4*max_vals[max_var_dim])/10

    right_center = np.array((max_vals + min_vals)/2)
    right_center[max_var_dim] = (6*max_vals[max_var_dim] + 4*min_vals[max_var_dim])/10

    return left_center, right_center, indices

  else:
      raise ValueError(f'distance metric {type(distance_metric).__name__} not supported')