import unittest
from datetime import date

from pynbp.gold_price_extractor import GoldPriceExtractor
import pandas as pd
import numpy as np


class TestGoldPriceExtractor(unittest.TestCase):

    def test_get_gold_prices(self):
        df = GoldPriceExtractor().get_gold_prices(start=date(2017, 8, 3), end=date(2021, 3, 13))
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(np.all(df.columns == ["date", "price_of_1g_of_gold_in_pln"]))


if __name__ == "__main__":
    unittest.main()
