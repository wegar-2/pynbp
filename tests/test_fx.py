from datetime import date
import pandas as pd
from pynbpapi.fx import get_fx_rates_for_currency
from pynbpapi.ccy import Ccy


def test_get_fx_rates_for_currency_usd():
    data = get_fx_rates_for_currency(
        ccy=Ccy.USD, start=date(2021, 3, 13), end=date(2022, 4, 15)
    )
    assert isinstance(data, pd.DataFrame)
    assert data.shape[1] == 2
    assert data.iloc[10, 1] == 3.957
