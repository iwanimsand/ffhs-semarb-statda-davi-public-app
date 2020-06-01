import os

import pandas as pd

data_path = os.path.join('./data/citibike/tripdata')


def read_df_month():
    hostname = os.uname()[1]
    # return pd.read_parquet(os.path.join(data_path, '201910-citibike-tripweather-data.parquet'))
    return pd.read_parquet(os.path.join(data_path, 'samples_5000_201910-citibike-tripweather-data.parquet'))
