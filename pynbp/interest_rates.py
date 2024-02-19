from datetime import datetime
from collections import defaultdict
import xml.etree.ElementTree as ElementTree
import requests
import numpy as np
import pandas as pd


RATES_NAMES_DICT: dict[str, str] = {
    "dys": "discount_rate", "dep": "deposit_rate", "lom": "lombard_rate",
    "ref": "reference_rate", "red": "rediscount_rate"
}


def get_interest_rates_table() -> pd.DataFrame:
    xml = load_xml()
    data_dict = parse_xml(xml=xml)
    return data_dict_to_dataframe(data_dict)


def load_xml() -> str:
    response = requests.get( # noqa
        "https://static.nbp.pl/dane/stopy/stopy_procentowe_archiwum.xml")
    response_text = response.text
    return response_text[response_text.find("<?xml version"):]


def parse_xml(xml: str):
    tree_root = ElementTree.fromstring(xml)
    entries = tree_root.findall("pozycje") # noqa
    data_dict = defaultdict(dict)
    for entry in entries:
        rates_list = []
        for el in entry.findall("pozycja"):
            rates_list.append((el.attrib["id"], el.attrib["oprocentowanie"]))
        data_dict[entry.attrib["obowiazuje_od"]] = dict(rates_list)
    rates_to_keep: list = list(RATES_NAMES_DICT.keys())
    out_dict = {}
    for k in data_dict:
        out_dict[k] = {
            el: float(data_dict[k][el].replace(",", "."))/100
            for el in rates_to_keep if el in data_dict[k].keys()
        }
        for rate in rates_to_keep:
            if rate not in out_dict[k].keys():
                out_dict[k][rate] = np.nan
    return out_dict


def data_dict_to_dataframe(data_dict: dict) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(data=data_dict, orient="index")
    df.index = [datetime.strptime(el, "%Y-%m-%d") for el in df.index]
    df.reset_index(inplace=True, drop=False)
    dict_cols_renaming = {
        **RATES_NAMES_DICT, **{"index": "valid_from_date"}
    }
    df.rename(columns=dict_cols_renaming, inplace=True)
    return df


if __name__ == "__main__":
    data = get_interest_rates_table()
    print(data)
