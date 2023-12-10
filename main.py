

from src.dataset_loader.file_reader import csv_reader, libsvm_reader
from src.dataset_loader.dataset import Dataset


csv_datasets = csv_reader("./datasets/adult.csv")
libsvm_datasets = libsvm_reader("./datasets/letter.scale")