
from typing import Sequence, Tuple
from typings.base_types import ArrayNxM, String
from os.path import exists
from pandas import read_csv # type: ignore
from numpy import hsplit
from sklearn.datasets import load_svmlight_file # type: ignore

def csv_reader(file_path: String) -> Tuple[ArrayNxM, ArrayNxM]:

  if not exists(file_path):
    raise FileNotFoundError(f'No file found at: {file_path}')

  dataset: Sequence[ArrayNxM] = hsplit(
          read_csv(# type: ignore
              file_path,
              header=None
          ).dropna().to_numpy(), [1]
      )

  labels, training_points = dataset

  return training_points, labels

def libsvm_reader(file_path: String) -> Tuple[ArrayNxM, ArrayNxM]:

  if not exists(file_path):
    raise FileNotFoundError(f'No file found at: {file_path}')


  points, labels = load_svmlight_file(file_path)# type: ignore

  points = points.toarray()# type: ignore

  return points, labels# type: ignore
