from musicrecolib.dataset import load_data

def test_dataset():
    df = load_data.LoadData().get_users_songs()
    assert df.shape == (11793648, 24)

def test_dataset_read():
    df = load_data.LoadData().get_users_songs()
    assert df['artist_name'][0] == 'Jorge Drexler'