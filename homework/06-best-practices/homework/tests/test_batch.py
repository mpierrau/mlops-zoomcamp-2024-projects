import pandas as pd
import batch
from deepdiff import DeepDiff
from utils import dt

def test_prepare_data() -> None:
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    expected_result = [
        (None,  None,   dt(1, 1),       dt(1, 10),      ((1-1)*60*60 + (10-1)*60 + 0)/60),
        (1,     1,      dt(1, 2),       dt(1, 10),      ((1-1)*60*60 + (10-2)*60 + 0)/60),
        (3,     4,      dt(1, 2, 0),    dt(2, 2, 1),    ((2-1)*60*60 + (2-2)*60 + 1-0)/60),
    ]

    expected_df = pd.DataFrame(expected_result, columns=df.columns.to_list() + ['duration'])

    actual_result = batch.prepare_data(df, df.columns)
    assert not DeepDiff(expected_df, actual_result)
