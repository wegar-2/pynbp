import unittest

import pandas as pd
import datetime as dt

from pynbp.fx_extractor import FxExtractor


class TestNbpFxRatesExtractor(unittest.TestCase):

    def test_get_fx_rates_for_currency_usd(self):
        extractor = FxExtractor()
        df = extractor.get_fx_rates_for_currency(
            iso_code="usd",
            start=dt.date(2021, 3, 13),
            end=dt.date(2022, 4, 15)
        )
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[1], 2)
        self.assertEqual(df.iloc[10, 1], 3.957)
        print("done")


if __name__ == "__main__":
    unittest.main()
