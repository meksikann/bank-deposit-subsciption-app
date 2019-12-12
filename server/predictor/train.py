import tensorflow as tf
import pandas as pd
from tensorflow import feature_column
from tensorflow.keras.layers import DenseFeatures, Dense, Dropout
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

import os
import helper as helper

print('TF version: ', tf.__version__)
# make sure trainer user right tf version
assert tf.__version__ == '2.0.0-rc1'

# load data into memory
dataset_path = 'data/bank-full.csv'
dataset = pd.read_csv(os.path.join(os.path.dirname(__file__), dataset_path),
                      delimiter=';', header=0, encoding='ascii', skipinitialspace=True)

# convert Y to INT
dataset['y'] = [1 if x == 'yes' else 0 for x in dataset['y']]

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
batch_size = 32
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


def get_model(first_feature_layer):
    model = tf.keras.Sequential([

        first_feature_layer,

        Dense(16, activation='relu'),
        Dropout(0.1),

        Dense(32, activation='relu'),
        Dropout(0.3),

        Dense(1, activation='sigmoid')
    ])

    return model


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

feature_layer = DenseFeatures(feature_columns)

model = get_model(feature_layer)

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

EPOCHS = 10
fit_history = model.fit(
    train_ds,
    verbose=1,
    epochs=EPOCHS,
    validation_data=test_ds
)

# ----------------------------------------------------------------------------------------
# ***************** Plot results**********************************************************
# ----------------------------------------------------------------------------------------
plt.title('Accuracy')
plt.plot(fit_history.history['accuracy'], color='blue', label='Train')
plt.plot(fit_history.history['val_accuracy'], color='orange', label='Val')
plt.legend()

_ = plt.figure()

plt.plot(fit_history.history['loss'], color='blue', label='Train')
plt.plot(fit_history.history['val_loss'], color='orange', label='Val')
plt.title('Loss')
plt.legend()

plt.show()
