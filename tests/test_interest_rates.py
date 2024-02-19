import numpy as np
import pandas as pd
from pynbp.interest_rates import get_interest_rates_table


def test_df_get_interest_rates_archive():
    data = get_interest_rates_table()
    assert isinstance(data, pd.DataFrame)
    assert data.shape[1] == 6
    assert (np.all(data.columns == [
            'valid_from_date', 'lombard_rate', 'reference_rate',
            'rediscount_rate', 'discount_rate', 'deposit_rate']
        ))
