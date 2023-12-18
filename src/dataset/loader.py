
from dataclasses import dataclass, field
from typing import Optional, Self
from os.path import join
from sklearn.compose import ColumnTransformer
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from typings.base_types import  ArrayNxM
from .file_reader import csv_reader, libsvm_reader
from .dataset import Dataset, DatasetParams

@dataclass
class DataLoader:
  params: DatasetParams

  def __post_init__(self: Self) -> None:
    self.col_transformer: ColumnTransformer = None

  def load_datasets(self: Self, base_dir: str) -> tuple[Dataset, Dataset]:

    training_set_path: str = join(base_dir, self.params['training_set'])
    test_set_path: str = join (base_dir, self.params['test_set'])

    if self.params['format'] == 'libsvm':
      training_dataset, training_label = libsvm_reader(training_set_path)
      test_dataset, test_label = libsvm_reader(test_set_path)
    elif self.params['format'] == 'csv':
      training_dataset, training_label = csv_reader(training_set_path)
      test_dataset, test_label = csv_reader(test_set_path)
    else:
      raise ValueError("Invalid dataset format. Only libsvm and csv are supported.")

    scaled_datasets = self.preprocess_data((training_dataset, test_dataset))

    end_feature_ix = len(self.col_transformer.named_transformers_['one_hot_encoder'].get_feature_names_out()) - 1

    return Dataset(scaled_datasets[0], training_label, end_feature_ix), \
           Dataset(scaled_datasets[1], test_label, end_feature_ix)


  def preprocess_data(self: Self,
                      dataset: tuple[ArrayNxM, ArrayNxM]) -> tuple[ArrayNxM, ArrayNxM]:

    whole_dataset= np.vstack(dataset)
    if not self.col_transformer:

      transformers: list[tuple[str, ColumnTransformer, list[int]]] = []

      categories_ix: list[int] = self.params['category_indexes'] if 'category_indexes' in self.params else []

      if categories_ix:
        transformers.append(('one_hot_encoder',
                            OneHotEncoder(categories='auto',drop='if_binary',
                                          sparse_output=False),
                            categories_ix))

      numerical_ix: list[int] = list(set(range(dataset[0].shape[1])) - set(categories_ix))

      transformers.append(('num_scaler',
                          MinMaxScaler(feature_range=(0.0, 1.0)),
                          numerical_ix))

      self.col_transformer = ColumnTransformer(transformers)
      whole_dataset = self.col_transformer.fit_transform(whole_dataset)

    else:
       whole_dataset = self.col_transformer.transform(whole_dataset)

    training_set, test_set = np.vsplit(whole_dataset, [dataset[0].shape[0]])

    return  training_set, test_set