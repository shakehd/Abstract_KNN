from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from sklearn.metrics import DistanceMetric
from typings.base_types import Label
from sys import argv
from os.path import exists, join
from tqdm import tqdm
from numpy import zeros
from pprint import pformat
from textwrap import indent
import logging
import argparse

from src.abstract_classifier.abstract_classifier import AbstractClassifier
from src.dataset.loader import DataLoader
from src.perturbation.adv_region import AdversarialRegion
from src.utils.configuration import Configuration

logger = logging.getLogger(__name__)

def main(params: Configuration, partition_size: int = 10,
         random_state: Optional[int] = None) -> None:
  @dataclass
  class Result:
    is_stable: bool
    is_robust: bool
    classification: set[Label]

  k_values = params['knn_params']['k_values']

  stable_count = zeros(len(k_values))
  robust_count = zeros(len(k_values))

  loader = DataLoader(params['dataset'])
  results: defaultdict[int, list[Result]] = defaultdict(list)

  training_set, test_set = loader.load_datasets(params['base_dirs']['dataset_dir'])

  distance_metric: DistanceMetric = DistanceMetric.get_metric(params['knn_params']['distance_metric'])
  abstract_classifier: AbstractClassifier = AbstractClassifier(distance_metric)
  abstract_classifier.fit(training_set, partition_size, random_state)

  progress_bar = tqdm(
      zip(test_set.points, test_set.labels),
      total=test_set.num_points,
      bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}{postfix}]',
      desc='Verifying'
  )

  epsilon = params['abstraction']['epsilon']

  classified_points = 0
  for (test_point, test_label) in progress_bar:
    logger.info("-- Classifying point %s %s with label %s --\n", classified_points + 1 , test_point, test_label)
    adv_region = AdversarialRegion(test_point, epsilon, test_set.num_feature_start_ix)

    logger.info("\tadversarial region: %s\n", adv_region)

    labels = abstract_classifier.get_classification(adv_region, k_values)

    logger.info('\tlabels: ')
    for k, item in labels.items():
      logger.info(f'\t\tk = {k} -> {item}', )
    logger.info('\n')

    for ix, (k, classification) in enumerate(labels.items()):

      is_stable = len(classification) == 1
      is_robust = is_stable and classification.pop() == test_label

      results[k].append(Result(is_stable, is_robust, classification))

      stable_count[ix] += is_stable
      robust_count[ix] += is_robust

    classified_points += 1
    progress_bar.set_postfix_str('ROB={}%, STAB={}%'.format(
          round(sum(robust_count) / (classified_points * len(k_values)) * 100, 1),
          round(sum(stable_count) / (classified_points * len(k_values)) * 100, 1)
    ))

    logger.info(f"-- Finished verifying point {classified_points} --\n")

  logger.info("\t Provable stability percentage :")
  logger.info('\t\t\n'.join([f'{k}: {robust_points/classified_points}' for robust_points, k in zip(robust_count, k_values)]))

if __name__ == "__main__":

  try:

    parser = argparse.ArgumentParser(description='Abstract Knn')
    parser.add_argument('configFilepath', metavar='CONFIGFILE',
                        help='name of the config file to read (it must be inside the config folder !!).')
    parser.add_argument('--random-state', metavar='RANDOM', type=int,
                        help='random state used when partitioning the dataset.')
    parser.add_argument('--partition-size', metavar='SIZE', type=int,
                        default=10,
                        help='max size of the data points in a partition (default 10).')
    parser.add_argument('--log ', dest='log_level',
                        choices=['INFO', 'DEBUG', 'ERROR'],
                        default='ERROR',
                        help='log level used during the verification phase (default ERROR).')

    args = parser.parse_args()

    params = Configuration()

    logging.basicConfig(filename='logs.log', filemode="w", level=args.log_level.upper(),
                        format="%(message)s")

    input_file_path = join(params['base_dirs']['config'], f'{argv[1]}.toml')
    if not exists(input_file_path):
      raise ValueError(f"Input file {input_file_path} not found:")

    params.load_settings(input_file_path)

    main(params, args.partition_size, args.random_state)

  except Exception:
    logger.exception('An error occurred: ')


