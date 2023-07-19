# PyNBP

This trivial package provides simple interface (consisting of three functions described below) 
that allows you to download the selected types of time series made available 
via [National Bank of Poland's API](http://api.nbp.pl/en.html).


More specifically, the following time series can be downloaded using PyNBP:

1. Average daily FX rates for select currencies 
(cf. [NBP's table of daily FX rates against various currencies]() 
for list of currencies for which exchange rates are published).
2. Table of historical central bank interest rates.
3. Gold prices in PLN (note: the gold prices published by NBP are prices of 1g of gold).

Strictly speaking, the table of historical interest is not provided via NBP's API.

I provide code snippets illustrating how to get the data below.


### Import PyNBP

```python
import pynbp
```

or:
```python
from pynbp import get_gold_prices, get_interest_rates_table, \
    get_fx_rates_for_currency
```

### Average daily FX rates
To download USDPLN daily average FX rates for the dates range 2018-01-03 to 2021-04-05 
(these dates are given in the ISO / %Y-%m-%d format) run:

```python
from pynbp import get_fx_rates_for_currency
from datetime import date
data = get_fx_rates_for_currency(
    iso_code="usd", 
    start=date(2018, 1, 3), 
    end=date(2021, 4, 5)
)
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


### Table of Historical Interest Rates
To download the table of historical interest rates set by NBP run:

```python
from pynbp import get_interest_rates_table
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
from pynbp import get_gold_prices
from datetime import date
data = get_gold_prices(
    start=date(2018, 1, 3), end=date(2021, 4, 5)
)
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
