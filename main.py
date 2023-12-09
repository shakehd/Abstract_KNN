

from src.dataset_loader.file_reader import csv_reader, libsvm_reader


csv_datasets = csv_reader("./datasets/adult.csv")
libsvm_datasets = libsvm_reader("./datasets/letter.scale")