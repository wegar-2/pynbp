from datetime import date

import pandas as pd

from pynbp.base_extractor import BaseExtractor


class GoldPriceExtractor(BaseExtractor):

    def __init__(self):
        super().__init__()

    def get_gold_prices(self, start: date, end: date):
        chunks = BaseExtractor.split_dates_range_into_smaller_chunks(start=start, end=end)
        dfs = []
        for start_, end_ in chunks:
            dfs.append(self._get_gold_prices_chunk(start=start_, end=end_))
        return pd.concat(dfs, axis=0).reset_index(drop=True, inplace=False).copy(deep=True)

    def _get_gold_prices_chunk(self, start: date, end: date) -> pd.DataFrame:
        return pd.DataFrame(
            data=self.run_web_api_query(url=self._get_gold_prices_url(start=start, end=end))
        ).rename(columns={"data": "date", "cena": "price_of_1g_of_gold_in_pln"}, inplace=False).copy(deep=True)

    def _get_gold_prices_url(self, start: date, end: date) -> str:
        return f"http://api.nbp.pl/api/cenyzlota/{start.isoformat()}/{end.isoformat()}/"


if __name__ == "__main__":
    gp_ex = GoldPriceExtractor()
    gp_ex.get_gold_prices(date(2017, 1, 1), date(2022, 7, 9))
