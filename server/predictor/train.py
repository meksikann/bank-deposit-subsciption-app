import tensorflow as tf
import pandas as pd
import os
print('TF version: ', tf.__version__)
# make sure trainer user right tf version
assert tf.__version__ == '2.0.0-rc1'

#load data into memory
dataset_path = 'data/bank-full.csv'
dataset = pd.read_csv(os.path.join(os.path.dirname(__file__), dataset_path))
print(dataset.head)

