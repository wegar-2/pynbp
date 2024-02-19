from datetime import date
import pandas as pd
from pynbp.fx import get_fx_rates_for_currency
from pynbp.currency import Currency


def test_get_fx_rates_for_currency_usd():
    data = get_fx_rates_for_currency(
        ccy=Currency.USD, start=date(2021, 3, 13), end=date(2022, 4, 15)
    )
    assert isinstance(data, pd.DataFrame)
    assert data.shape[1] == 2
    assert data.iloc[10, 1] == 3.957
