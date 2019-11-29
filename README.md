# mayacal
WORK IN PROGRESS - Implementation of some datetime features for Classical Maya calendar

Requires Python 3.5+

Example Usage:

```python

>>> lc = LongCount(9, 0, 0, 0, 0)
>>> lc.get_calendar_round()

8 Ajaw 13 Keh

```


```python

>>> lc_1 = LongCount(9, 12, 13, 0, 5)
>>> lc_2 = LongCount(8, 0, 0, 0, 0)
>>> diff = (lc_1 - lc_2)
>>> diff
1.12.13.0.5

>>> diff.get_total_kin()
235085
```
