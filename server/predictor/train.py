import tensorflow as tf
import pandas as pd
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import os
import helper as helper

print('TF version: ', tf.__version__)
# make sure trainer user right tf version
assert tf.__version__ == '2.0.0-rc1'

# load data into memory
dataset_path = 'data/bank-full.csv'
dataset = pd.read_csv(os.path.join(os.path.dirname(__file__), dataset_path),
                      delimiter=';', header=0, encoding='ascii')

# find if there are some empty cells
null_columns = dataset.columns[dataset.isnull().any()]
dataset[null_columns].isnull().sum()
print(null_columns)

df_with_nan = dataset[dataset.isnull().any(axis=1)][null_columns]
print(df_with_nan)

assert df_with_nan.empty == True

# ----------------------------------------------------------------------------------------
# Data preprocessing
# ----------------------------------------------------------------------------------------
print(dataset.columns.tolist())
train, test = train_test_split(dataset, test_size=0.3)

print(len(train), 'train set length.')
print(len(test), 'test set length.')


# we will wrap the dataframes with tf.data. This will enable us to use feature columns as a bridge to map from the
# columns in the Pandas dataframe to features used to train the model. If we were working with a very large CSV file
# (so large that it does not fit into memory), we would use tf.data to read it from disk directly
batch_size = 5
train_ds = helper.df_to_dataset(train, batch_size=batch_size)
test_ds = helper.df_to_dataset(test, batch_size=batch_size, shuffle=False)
for feature, label in test_ds.take(1):
    print('feature batch:', list(feature.keys()))
    print('batch of jobs:', feature['job'])
    print('labels batch:', label)
# ----------------------------------------------------------------------------------------
# Create, train and evaluate model
# ----------------------------------------------------------------------------------------
