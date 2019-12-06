import tensorflow as tf
import pandas as pd
from tensorflow import feature_column
from tensorflow.keras.layers import DenseFeatures
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
# ********************************** Data preprocessing **********************************
# ----------------------------------------------------------------------------------------
print(dataset.columns.tolist())
train, test = train_test_split(dataset, test_size=0.3)

print(len(train), 'train set length.')
print(len(test), 'test set length.')

# ----------------------------------------------------------------------------------------
# Input pipeline
# ----------------------------------------------------------------------------------------

# we will wrap the dataframes with tf.data. This will enable us to use feature columns as a bridge to map from the
# columns in the Pandas dataframe to features used to train the model. If we were working with a very large CSV file
# (so large that it does not fit into memory), we would use tf.data to read it from disk directly
batch_size = 5
train_ds = helper.df_to_dataset(train, batch_size=batch_size)
test_ds = helper.df_to_dataset(test, batch_size=batch_size, shuffle=False)

# define feature types
num_f = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']
bucket_f = ['age']  # numerical features to bucketize
categorical_f = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'poutcome']


# min max scaler (possible to use sklearm scaler in future)
def scale_feature(data_set, feature):
    def minmax(x):
        min_val = data_set[feature].min()
        max_val = data_set[feature].max()
        return (x - min_val) / (max_val - min_val)

    return minmax


# create feature columns
feature_columns = []
for header in num_f:
    scaled_f = scale_feature(train, header)
    feature_columns.append(feature_column.numeric_column(header, normalizer_fn=scaled_f))

age_boundaries = [18, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
age = feature_column.numeric_column('age')
buck_age = feature_column.bucketized_column(age, boundaries=age_boundaries)
feature_columns.append(buck_age)

for feature_name in categorical_f:
    vocabulary = dataset[feature_name].unique()
    cat_col = tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary)
    one_hot = feature_column.indicator_column(cat_col)
    feature_columns.append(one_hot)

# ----------------------------------------------------------------------------------------
# ***************** Create, train and evaluate model *************************************
# ----------------------------------------------------------------------------------------
# TODO: remove example_batch
example_batch = next(iter(train_ds))[0]


feature_layer = DenseFeatures(feature_columns)
print(feature_layer(example_batch).numpy())
