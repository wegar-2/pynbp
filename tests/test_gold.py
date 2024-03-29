from datetime import date
import numpy as np
import pandas as pd
from pynbp.gold import get_gold_prices


def test_get_gold_prices():
    data = get_gold_prices(start=date(2017, 8, 3), end=date(2021, 3, 13))
    assert isinstance(data, pd.DataFrame)
    assert np.all(data.columns == ["date", "price_of_1g_of_gold_in_pln"])
