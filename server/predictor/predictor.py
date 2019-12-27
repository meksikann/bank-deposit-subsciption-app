import tensorflow as tf
import pandas as pd
from tensorflow import feature_column
from tensorflow.keras.layers import DenseFeatures, Dense, Dropout, concatenate
from sklearn.model_selection import train_test_split
from tensorflow import keras

import matplotlib.pyplot as plt
import os

print('TF version: ', tf.__version__)
# make sure trainer user right tf version
assert tf.__version__ == '2.0.0-rc1'
MODEL_NAME = 'model/my_model_v4'
MODEL_NAME_H5 = 'model/my_model_v4.hdf5'
MODEL_JSON = 'model/model_config.json'
MODEL_PATH = os.path.join(os.path.dirname(__file__), MODEL_NAME)
MODEL_JSON_PATH = os.path.join(os.path.dirname(__file__), MODEL_JSON)
MODEL_PATH_H5 = os.path.join(os.path.dirname(__file__), MODEL_NAME_H5)
WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), 'weights/deposit-v2.h5')

def run_train():
    import helper as helper

    # load data into memory
    dataset_path = 'data/bank-full.csv'
    dataset = pd.read_csv(os.path.join(os.path.dirname(__file__), dataset_path),
                          delimiter=';', header=0, encoding='ascii', skipinitialspace=True)

    # convert Y to INT
    dataset['y'] = [1 if x == 'yes' else 0 for x in dataset['y']]

    # find if there are some empty cells
    null_columns = dataset.columns[dataset.isnull().any()]
    dataset[null_columns].isnull().sum()

    df_with_nan = dataset[dataset.isnull().any(axis=1)][null_columns]

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
            Dropout(0.2),

            Dense(16, activation='relu'),
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

    EPOCHS = 1
    fit_history = model.fit(
        train_ds,
        verbose=1,
        epochs=EPOCHS,
        validation_data=test_ds
    )
    print('Save all model data')
    # model.save(MODEL_PATH, save_format='tf')
    model.save(MODEL_PATH_H5)
    # tf.saved_model.save(model, MODEL_PATH)
    # model.save_weights(WEIGHTS_PATH)


    # json_config = model.to_json()
    #
    # # save model configs and and arch
    # with open(MODEL_JSON_PATH, 'w') as json_file:
    #     json_file.write(json_config)
    # model.save_weights(WEIGHTS_PATH)

    # ----------------------------------------------------------------------------------------
    # ***************** Plot results**********************************************************
    # ----------------------------------------------------------------------------------------
    plt.title('Accuracy')
    plt.plot(fit_history.history['accuracy'], color='blue', label='Train')
    plt.plot(fit_history.history['val_accuracy'], color='red', label='Validation')
    plt.legend()

    _ = plt.figure()

    plt.plot(fit_history.history['loss'], color='blue', label='Train')
    plt.plot(fit_history.history['val_loss'], color='orange', label='Validation')
    plt.title('Loss')
    plt.legend()

    plt.show()


def channel_zeropad(x, channel_axis=3):
    '''
    Zero-padding for channle dimensions.
    Note that padded channles are added like (Batch, H, W, 2/x + x + 2/x).
    '''
    shape = list(x.shape)
    y = K.zeros_like(x)

    if channel_axis == 3:
        y = y[:, :, :, :shape[channel_axis] // 2]
    else:
        y = y[:, :shape[channel_axis] // 2, :, :]

    return concatenate([y, x, y], channel_axis)



def channel_zeropad_output(input_shape, channel_axis=3):
    '''
    Function for setting a channel dimension for zero padding.
    '''
    shape = list(input_shape)
    shape[channel_axis] *= 2

    return tuple(shape)




def predict_users(data):
    import predictor.helper as helper


    print('load model....')

    users_df = helper.preprocess_data_to_df(data['users'])

    # with open(MODEL_JSON_PATH) as json_file:
    #     json_config = json_file.read()
    # model = tf.keras.models.model_from_json(json_config)
    # model.load_weights(WEIGHTS_PATH)

    model = keras.models.load_model(MODEL_PATH_H5)
    print('Model loaded....')

    model.summary()
    pred = model.predict(users_df)
    print(pred)
    return []


# run only as script
if __name__ == '__main__':
    run_train()
