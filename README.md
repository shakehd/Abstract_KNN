# Robustness Verification of *k*-Nearest Neighbors

Implementation of an abstract interpretation-based tool for proving robustness and stability properties of *k*NN classifiers.

## Requirements
- Python3

## Installation
To install this toool you need to clone or download this repository and run the commands:
```[bash]
pip install -r requirements.txt
```
This will install the following dependencies:
- joblib version 1.3.2
- nptyping version 2.5.0
- numpy version 1.26.1
- pandas version 2.1.3
- python-dateutil version 2.8.2
- pytz version 2023.3.post1
- scikit-learn version 1.3.2
- scipy version 1.12.0
- six version 1.16.0
- threadpoolctl version 3.2.0
- tomli version 2.0.1
- tqdm version 4.66.1
- tzdata version 2023.4

## Usage

To run this tool simply launch the following command inside the repo folder:

```[bash]
python abstract_classifier.py CONFIGFILE <arguments>
```
where `CONFIGFILE` is a config file present inside the `configs` folder (or the
one configured in the `.settings.toml` configuration file), meanwhile `<arguments>`
can be one of the following:

|  Arg | Description  |
|---|---|
| --random-state RANDOM | Random seed used when partitioning the dataset. |
| --partition-size SIZE | Maximum number of data points in a partition (default 20). |
| --log  {INFO,DEBUG,ERROR}  | Log level used during the verification phase (default ERROR).  |
| -h, --help  | Show help message and exit.  |


## Results
After the verification process is finished the tool will save the results in 4 files:
- **classification.csv**: Contains the classifications results for each value of k.
- **robustness.csv**: Contains the robustness results for each value of k.
- **stability.csv**: Contains the stability results for each value of k.
- **overall_result.csv**: Contains the overall robustness and stability percentage and
                          runtime information.

## Configurations

The tool requires two configuration files to work properly:

- settings.toml: A TOML configuration file specifying the folders containing the datasets
                 and configurations for the verification process of a dataset.

- *verification*.toml: A TOML configuration file specifying the settings needed to verify a
                     a dataset.

### settings.toml

The settings.toml has the following form:
```
[base_dirs]
config = "./configs"
dataset = "./datasets"
result = "./results"
logs = "./logs""
```
where the `base_dirs` contains the following settings:

- `config`: directory where the configuration files are located (default ./config).
- `dataset_dir`: directory where datasets are located  (default ./dataset).
- `result`: directory where the verification results are saved  (default ./result).
- `logs`: directory where the logs are saved  (default ./logs).

### verification.toml

The *verification*.toml has the following form:
```
[knn_params]
k_values = [list of k values]
distance_metric = "distance metric (euclidean or manhattan)"

[dataset]
format = "dataset format (libsvm or csv)"
training_set = "training dataset name"
test_set = "test dataset name"

[abstraction]
epsilon = epsilon value
```
It has three section:

- `knn_params`:
  - `k_values`: list of possible values for the number of nearest neighbors to consider for each prediction.
  - `distance_metric`: The metric used to measure the distance between data points

- `dataset`:
  - `format`: The format of the dataset which can be *libsvm* or *csv*.
  - `training_set`: The name of the file that contains the training data
  - `test_set`:  The name of the file that contains the test data

- `abstraction`:
  - `epsilon`: The perturbation value.
