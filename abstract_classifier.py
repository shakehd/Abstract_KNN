from collections import defaultdict
import csv
from dataclasses import dataclass
from typing import Optional
from sklearn.metrics import DistanceMetric
from sys import argv
from os.path import exists, join
from os import mkdir
from tqdm import tqdm
from numpy import zeros
import logging
import argparse
import time

from src.abstract.classifier import AbstractClassifier
from src.dataset.loader import DataLoader
from src.perturbation.adv_region import AdversarialRegion
from src.utils.configuration import Configuration

logger = logging.getLogger(__name__)

def get_args_parser() -> argparse.ArgumentParser:

  parser = argparse.ArgumentParser(description='Abstract Knn')
  parser.add_argument('config_filepath', metavar='CONFIGFILE',
                      help='name of the config file to read (it must be inside the config folder !!).')
  parser.add_argument('--random-state', metavar='RANDOM', type=int,
                      help='random seed used when partitioning the dataset.')
  parser.add_argument('--partition-size', metavar='SIZE', type=int,
                      default=20,
                      help='maximum number of data points in a partition (default 20).')
  parser.add_argument('--log ', dest='log_level',
                      choices=['INFO', 'DEBUG', 'ERROR'],
                      default='ERROR',type = str.upper,
                      help='log level used during the verification phase (default ERROR).')

  return parser


def main(params: Configuration, partition_size: int = 20,
         random_state: Optional[int] = None) -> None:

  k_values = params['knn_params']['k_values']

  stable_count = zeros(len(k_values))
  robust_count = zeros(len(k_values))

  loader = DataLoader(params['dataset'])

  training_set, test_set = loader.load_datasets(params['base_dirs']['dataset'])

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
  classification_results: list[list[str]]  = []
  robustness_results: list[list[str]]      = []
  stability_results: list[list[str]]       = []

  clock_st: float = time.time()
  process_st: float = time.process_time()

  for (test_point, test_label) in progress_bar:
    logger.info("-- Classifying point %s %s with label %s --\n", classified_points + 1 , test_point, test_label)
    adv_region = AdversarialRegion(test_point, epsilon, test_set.num_feature_start_ix)

    logger.info("\tadversarial region: %s\n", adv_region)

    labels = abstract_classifier.get_classification(adv_region, k_values)

    classification_result: list[str]  = [str(classified_points+1), str(test_label)]
    robustness_result: list[str]      = [str(classified_points+1)]
    stability_result: list[str]       = [str(classified_points+1)]

    logger.info('\tlabels: ')
    for ix, (k, classification) in enumerate(labels.items()):

      logger.info(f'\t\tk = {k} -> {classification}', )
      classification_result.append(str(classification))

      is_stable = len(classification) == 1
      is_robust = is_stable and classification.pop() == test_label

      robustness_result.append('Yes' if is_robust else 'No')
      stability_result.append('Yes' if is_stable else 'No')

      stable_count[ix] += is_stable
      robust_count[ix] += is_robust

    logger.info('\n')

    classification_results.append(classification_result)
    robustness_results.append(robustness_result)
    stability_results.append(stability_result)

    classified_points += 1
    progress_bar.set_postfix_str('ROB={}%, STAB={}%'.format(
          round(sum(robust_count) / (classified_points * len(k_values)) * 100, 1),
          round(sum(stable_count) / (classified_points * len(k_values)) * 100, 1)
    ))

  logger.info(f"-- Finished verifying point {classified_points} --\n")

  elapsed_clock: float = time.time() - clock_st
  elapsed_process: float = time.process_time() - process_st

  overall_results: list[list[str]] = [['Overall stability percentage'] +\
      [f'{(stable_points/classified_points)*100}' for stable_points in stable_count]]

  overall_results.append(['Overall robustness percentage'] +\
      [f'{(robust_points/classified_points)*100}' for robust_points in robust_count])

  overall_results.append(['']*len(k_values))
  overall_results.append(['runtime (clock time)', f'{time.strftime("%H:%M:%S", time.gmtime(elapsed_clock))}']+\
                          ['']*(len(k_values)-1))
  overall_results.append(['runtime (process time)', f'{time.strftime("%H:%M:%S", time.gmtime(elapsed_process))}']+\
                          ['']*(len(k_values)-1))

  results_dir = params['base_dirs']['result']
  with open(join(results_dir, 'classification.csv'), 'w', newline='', encoding='utf-8') as classification_file,\
       open(join(results_dir, 'robustness.csv'), 'w', newline='', encoding='utf-8') as robustness_file,\
       open(join(results_dir, 'stability.csv'), 'w', newline='', encoding='utf-8') as stability_file,\
       open(join(results_dir, 'overall_result.csv'), 'w', newline='', encoding='utf-8') as overall_result_file:

    classification_writer = csv.writer(classification_file)
    classification_header = ['Test point #', 'Actual Classification'] + [f' Classification at K={k}' for k in k_values]
    classification_writer.writerow(classification_header)

    robustness_writer = csv.writer(robustness_file)
    robustness_header = ['Test point #'] + [f'Robustness at K={k}' for k in k_values]
    robustness_writer.writerow(robustness_header)

    stability_writer = csv.writer(stability_file)
    stability_header = ['Test point #'] + [f'Stability at K={k}' for k in k_values]
    stability_writer.writerow(stability_header)

    overall_result_writer = csv.writer(overall_result_file)
    overall_result_header = ['At'] + [f'K={k}' for k in k_values]
    overall_result_writer.writerow(overall_result_header)

    classification_writer.writerows(classification_results)
    robustness_writer.writerows(robustness_results)
    stability_writer.writerows(stability_results)
    overall_result_writer.writerows(overall_results)

if __name__ == "__main__":

  try:

    args = get_args_parser().parse_args()

    params = Configuration()

    if not exists(params['base_dirs']['logs']):
      mkdir(params['base_dirs']['logs'])

    logging.basicConfig(filename=join(params['base_dirs']['logs'], 'logs.log'),
                        filemode="w", level=args.log_level.upper(), format="%(message)s")

    input_file_path = join(params['base_dirs']['config'], f'{args.config_filepath}.toml')
    if not exists(input_file_path):
      raise ValueError(f"Input file {input_file_path} not found:")

    params.load_configuration(input_file_path)

    if not exists(params['base_dirs']['result']):
      mkdir(params['base_dirs']['result'])

    main(params, args.partition_size, args.random_state)

  except Exception:
    logger.exception('An error occurred: ')


