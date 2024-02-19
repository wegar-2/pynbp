import datetime as dt
import xml.etree.ElementTree as ElementTree
import requests
import numpy as np
import pandas as pd


class InterestRatesExtractor:

    RATES_NAMES_DICT: dict[str, str] = {
        "dys": "discount_rate", "dep": "deposit_rate",
        "lom": "lombard_rate", "ref": "reference_rate",
        "red": "rediscount_rate"
    }

    def __init__(self):
        self.str_xml = None
        self.data_dict = None
        self.df = None

    def load_interest_rates_archive(self):
        self.load_xml()
        self.parse_xml()
        df = self.data_dict_to_dataframe()
        self.df = df

    def get_interest_rates_table(self) -> pd.DataFrame:
        if self.df is None:
            self.load_interest_rates_archive()
        return self.df

    def data_dict_to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(data=self.data_dict, orient="index")
        df.index = [dt.datetime.strptime(el, "%Y-%m-%d") for el in df.index]
        df.reset_index(inplace=True, drop=False)
        dict_cols_renaming = {
            **self.RATES_NAMES_DICT, **{"index": "valid_from_date"}
        }
        df.rename(columns=dict_cols_renaming, inplace=True)
        return df

    def load_xml(self):
        response = requests.get(
            "https://static.nbp.pl/dane/stopy/stopy_procentowe_archiwum.xml")
        response_text = response.text
        self.str_xml = response_text[response_text.find("<?xml version"):]

    def parse_xml(self):
        tree_root = ElementTree.fromstring(self.str_xml)
        l_entries = tree_root.findall("pozycje")
        data_dict = {l_entries[k].attrib["obowiazuje_od"]: [] for k in range(len(l_entries))}
        for entry in l_entries:
            iter_list = []
            l_data = entry.findall("pozycja")
            for data_elem in l_data:
                iter_list.append((
                    data_elem.attrib["id"],
                    data_elem.attrib["oprocentowanie"]
                ))
            data_dict[entry.attrib["obowiazuje_od"]] = dict(iter_list)
        l_rates_to_keep = list(self.dict_rates_names.keys())
        for iter_key, iter_el in data_dict.items():
            data_dict[iter_key] = {
                el: float(data_dict[iter_key][el].replace(",", "."))/100
                for el in l_rates_to_keep if el in data_dict[iter_key].keys()
            }
            for iter_rate in l_rates_to_keep:
                if iter_rate not in data_dict[iter_key].keys():
                    data_dict[iter_key][iter_rate] = np.nan
        self.data_dict = data_dict
