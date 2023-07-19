import unittest
import pandas as pd
import numpy as np

from pynbp.interest_rates_extractor import InterestRatesExtractor


class TestInterestRatesExtractor(unittest.TestCase):

    def test_df_get_interest_rates_archive(self):
        extractor = InterestRatesExtractor()
        extractor.load_interest_rates_archive()
        df = extractor.get_interest_rates_table()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[1], 6)
        self.assertTrue(
            np.all(df.columns == [
                'valid_from_date', 'lombard_rate', 'reference_rate', 'rediscount_rate',
                'discount_rate', 'deposit_rate'
            ])
        )


if __name__ == "__main__":
    unittest.main()
