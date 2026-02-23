# pynbpapi

![Flake8 Lint Check](https://github.com/wegar-2/pynbp/actions/workflows/flake8-lint.yml/badge.svg)
![CI](https://github.com/wegar-2/pynbp/actions/workflows/python-tests.yml/badge.svg)
[![codecov](https://codecov.io/github/wegar-2/pynbp/graph/badge.svg?token=XJY6OWPSPI)](https://codecov.io/github/wegar-2/pycs)


This trivial package provides simple interface (consisting of three functions described below) 
that allows you to download the selected types of time series made available 
via [National Bank of Poland's REST API](http://api.nbp.pl/en.html).


More specifically, the following time series can be downloaded using PyNBP:

1. Average daily FX rates for select currencies 
(cf. [NBP's table of daily FX rates against various currencies]() 
for list of currencies for which exchange rates are published).
2. Table of historical central bank interest rates.
3. Gold prices in PLN (note: the gold prices published by NBP are prices of 1g of gold).
4. Downloading of the daily central bank's [FX rates tables](https://nbp.pl/statystyka-i-sprawozdawczosc/kursy/) (A, B and C)

Note: the table of historical interest is not *per se* provided via NBP's API.

I provide code snippets illustrating how to get the data below.


### Import py-NBP-API

```python
import pynbpapi
```

or:

```python
from pynbpapi import (
    get_gold_prices, get_interest_rates_table, get_fx_rate,
    get_nbp_fx_tables, get_fx_rates)
```

### FX rate for a single pair against PLN
To download USDPLN daily average FX rates for the dates range 2018-01-03 to 2021-04-05 
(these dates are given in the ISO / %Y-%m-%d format) run:

```python
from pynbpapi import get_fx_rate
from datetime import date

data = get_fx_rate(ccy="usd", start=date(2018, 1, 3), end=date(2021, 4, 5))
print(data.head())
```

Output:
```
         date  usdpln_rate
0  2018-01-03       3.4616
1  2018-01-04       3.4472
2  2018-01-05       3.4488
3  2018-01-08       3.4735
4  2018-01-09       3.4992
```

### FX rates for multiple pairs against PLN
To download USDPLN, EURPLN and CNYPLN daily average FX rates for the dates 
range 2018-01-03 to 2021-04-05 
(these dates are given in the ISO / %Y-%m-%d format)
in the long format (alternatively - wide format can be chosen) run:

```python
from pynbpapi import get_fx_rates, Ccy
from datetime import date

data = get_fx_rates(
    ccys=[Ccy.EUR, Ccy.USD, Ccy.CNY],
    start=date(2018, 1, 3),
    end=date(2021, 4, 5), 
    fmt="long"
)
print(data.head())
print(data.tail())
```

Output - head:
```
         date    rate    pair
0  2018-01-03  4.1673  eurpln
1  2018-01-04  4.1515  eurpln
2  2018-01-05  4.1544  eurpln
3  2018-01-08  4.1647  eurpln
4  2018-01-09  4.1779  eurpln
```
And tail:
```
           date    rate    pair
816  2021-03-29  0.6027  cnypln
817  2021-03-30  0.6030  cnypln
818  2021-03-31  0.6053  cnypln
819  2021-04-01  0.5998  cnypln
820  2021-04-02  0.5941  cnypln
```



### Table of Historical Interest Rates
To download the table of historical interest rates set by NBP run:

```python
from pynbpapi import get_interest_rates_table
from datetime import date

data = get_interest_rates_table()
print(data.tail())
```

Output:
```
   valid_from_date  lombard_rate  reference_rate  rediscount_rate  discount_rate  deposit_rate
82      2022-04-07        0.0500          0.0450           0.0455         0.0460        0.0400
83      2022-05-06        0.0575          0.0525           0.0530         0.0535        0.0475
84      2022-06-09        0.0650          0.0600           0.0605         0.0610        0.0550
85      2022-07-08        0.0700          0.0650           0.0655         0.0660        0.0600
86      2022-09-08        0.0725          0.0675           0.0680         0.0685        0.0625
```



### Gold Prices in PLN
To download gold prices in PLN for the dates range 2018-01-03 to 2021-04-05 run:

```python
from pynbpapi import get_gold_prices
from datetime import date

data = get_gold_prices(start=date(2018, 1, 3), end=date(2021, 4, 5))
print(data.head())
```

Please keep in mind that the daily prices of gold published by 
NBP are prices of 1g of gold in PLN. 

Output:
```
         date  price_of_1g_of_gold_in_pln
0  2018-01-03                      145.72
1  2018-01-04                      146.36
2  2018-01-05                      145.68
3  2018-01-08                      146.06
4  2018-01-09                      147.42
```


### Download Daily NBP's FX Rates Tables 
To download FX rates table A for dates range 2026-02-18 to 2026-02-19 run:

```python
from pynbpapi import get_nbp_fx_tables
from datetime import date
data = get_nbp_fx_tables(table="A", start=date(2026, 2, 18), end=date(2026, 2, 19))
```

Please keep in mind that the daily prices of gold published by 
NBP are prices of 1g of gold in PLN. 

Output - head:
```
             currency code     mid table              no        date
0     bat (Tajlandia)  THB  0.1137     A  033/A/NBP/2026  2026-02-18
1   dolar amerykański  USD  3.5610     A  033/A/NBP/2026  2026-02-18
2  dolar australijski  AUD  2.5204     A  033/A/NBP/2026  2026-02-18
3     dolar Hongkongu  HKD  0.4556     A  033/A/NBP/2026  2026-02-18
4    dolar kanadyjski  CAD  2.6078     A  033/A/NBP/2026  2026-02-18
```

And tail:
```
                   currency code       mid table              no        date
59       rupia indonezyjska  IDR  0.000212     A  034/A/NBP/2026  2026-02-19
60           rupia indyjska  INR  0.039242     A  034/A/NBP/2026  2026-02-19
61  won południowokoreański  KRW  0.002472     A  034/A/NBP/2026  2026-02-19
62    yuan renminbi (Chiny)  CNY  0.515200     A  034/A/NBP/2026  2026-02-19
63                SDR (MFW)  XDR  4.909800     A  034/A/NBP/2026  2026-02-19
```