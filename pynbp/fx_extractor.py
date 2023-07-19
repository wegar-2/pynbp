from datetime import date

import pandas as pd
import logging

from pynbp.base_extractor import BaseExtractor
from pynbp.constants import allowed_foreign_currencies_iso_codes


logger = logging.getLogger(__name__)


class FxExtractor(BaseExtractor):

    def __init__(self):
        super().__init__()

    @staticmethod
    def _parse_json(json_) -> pd.DataFrame:
        return pd.DataFrame(data=json_["rates"]).rename(
            columns={"effectiveDate": "date", "mid": "rate"}).drop(columns=["no"], inplace=False)

    @staticmethod
    def _get_api_query(iso_code: str, start: date, end: date) -> str:
        return f"http://api.nbp.pl/api/exchangerates" \
               f"/rates/a/{iso_code}/{start.isoformat()}/{end.isoformat()}/"

    def get_fx_rates_for_currency(self, iso_code: str, start: date, end: date) -> pd.DataFrame:
        if iso_code.lower() not in allowed_foreign_currencies_iso_codes:
            raise ValueError(
                f"Invalid parameters iso_code passed to function "
                f"{self.get_fx_rates_for_currency.__name__} of class {self.__class__.__name__}!"
            )
        chunks = self.split_dates_range_into_smaller_chunks(start=start, end=end)
        list_dfs = []
        for start_, end_ in chunks:
            list_dfs.append(self._parse_json(
                json_=self.run_web_api_query(
                    url=self._get_api_query(iso_code=iso_code, start=start_, end=end_))
            ))
        return pd.concat(list_dfs, axis=0).rename(
            columns={"rate": f"{iso_code}pln_rate"}, inplace=False).reset_index(
            inplace=False, drop=True
        ).copy(deep=True)


if __name__ == "__main__":
    ex = FxExtractor()
    res = ex.get_fx_rates_for_currency(iso_code="usd", start=date(2017, 11, 18), end=date(2022, 7, 18))
