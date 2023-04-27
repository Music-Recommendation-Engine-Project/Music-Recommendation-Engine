import pandas as pd

def test_dataset():
    df = pd.read_parquet("user_track_df.parquet", engine='pyarrow')
    assert df.shape == (11793648, 24)

def test_dataset_read():
    df = pd.read_parquet("user_track_df.parquet", engine='pyarrow')
    assert df['artist_name'][0] == 'Jorge Drexler'