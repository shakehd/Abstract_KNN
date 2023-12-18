from typings.base_types import ArrayNxM, String
from os.path import exists
from pandas import read_csv
from numpy import hsplit
from sklearn.datasets import load_svmlight_file

def csv_reader(file_path: String) -> tuple[ArrayNxM, ArrayNxM]:

  if not exists(file_path):
    raise FileNotFoundError(f'No file found at: {file_path}')

  dataset: list[ArrayNxM] = hsplit(
          read_csv(
              file_path,
              header=None
          ).dropna().to_numpy(), [1]
      )

  labels, training_points = dataset

  return training_points, labels.reshape((-1,))

def libsvm_reader(file_path: String) -> tuple[ArrayNxM, ArrayNxM]:

  if not exists(file_path):
    raise FileNotFoundError(f'No file found at: {file_path}')

  points, labels = load_svmlight_file(file_path)

  points = points.toarray()

  return points, labels
