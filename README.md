# mayacal
WORK IN PROGRESS - Implementation of some calendrical features for Classical Maya calendar

Requires Python 3.5+

## Installation

```shell

pip install mayacal

```



## Example Usage:

Import:

``` python

>>> import mayacal as mc

```

Basic conversions and additions:
```python

>>> lc = mc.LongCount(9, 0, 0, 0, 0)
>>> lc.get_calendar_round()
8 Ajaw 13 Keh

>>> dist = mc.DistanceNumber(mc.LongCount(0, 0, 13, 2, 10), sign=1)
>>> new_lc = lc + dist
>>> new_lc
9.0.13.2.10

>>> new_lc.get_mayadate()
9.0.13.2.10  6 Ok 18 Sak

>>> print(new_lc.to_julian())
Nov 19, 448 CE

>>> print(new_lc.to_gregorian())
Nov 20, 448 CE

```

Get all Long Count dates corresponding to a given Calendar Round:
```python

>>> cr = mc.CalendarRound(mc.Tzolkin(6, "Ok"), mc.Haab(18, "Sak"))
>>> min_lc = mc.LongCount(9,0,0,0,0)
>>> max_lc = mc.LongCount(10,0,0,0,0)
>>> cr.get_long_count_possibilities(min_lc, max_lc)
[9.0.13.2.10, 9.3.5.15.10, 9.5.18.10.10, 9.8.11.5.10, 9.11.4.0.10, 9.13.16.13.10, 9.16.9.8.10, 9.19.2.3.10]

```

Find the distance between two Long Count dates:
```python

>>> lc_1 = mc.LongCount(9, 12, 13, 0, 5)
>>> lc_2 = mc.LongCount(8, 0, 0, 0, 0)
>>> diff = (lc_1 - lc_2)
>>> diff
1.12.13.0.5

>>> diff.get_total_kin()
235085

>>> diff.to_approx_years(pretty_print=True)
'643 years, 7 months, 16 days'

```

Infer missing date components:
```python

>>> cr = mc.CalendarRound(mc.Tzolkin(4, "Ajaw"), mc.Haab(8, "Kumku"))
>>> lc = mc.LongCount(9, 4, None, 10, None)
>>> date = mc.Mayadate(lc, cr)
>>> date.infer_mayadates()
[9.4.10.10.0  4 Ajaw 8 Kumku]

```

```python

>>> cr = mc.CalendarRound(mc.Tzolkin(4, "Ajaw"), mc.Haab(8, "Kumku"))
>>> lc = mc.LongCount(9,None,None,None,None)
>>> date = mc.Mayadate(lc, cr, glyph_g='G3')
>>> date.infer_mayadates()
[9.1.17.15.0  4 Ajaw 8 Kumku]

```

```python

>>> cr = mc.CalendarRound(mc.Tzolkin(4, "Ajaw"), haab=None)
>>> lc = mc.LongCount(10,None,8,10,None)
>>> date = mc.Mayadate(lc, cr)
>>> date.infer_long_count_dates()
[10.1.8.10.0, 10.14.8.10.0]

```

## Development

### Dependencies
There are currently no external dependencies outside of the standard python library. Note the the package requires Python 3.5 or later.


### Testing (WIP)
Testing is implemented via [pytest](https://docs.pytest.org/en/latest/index.html).

After installing pytest, you can run all the tests in the package using the following command:
```shell
python -m py.test
```

To run tests in a specific file, use:
```shell
python -m py.test tests/...PATH_TO_TEST_FILE... 
```

