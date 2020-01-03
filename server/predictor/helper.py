import tensorflow as tf
import pandas as pd


def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop('y')

    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))

    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)

    return ds


def preprocess_data_to_df(data, batch_size=32):
    print('Start data preprocessing  -------------->>>>>>>')
    df = pd.DataFrame(data)
    df = tf.data.Dataset.from_tensor_slices((dict(df)))
    df = df.batch(batch_size)

    return df
