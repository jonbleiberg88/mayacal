import math
import datetime


class JulianDate:

    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def to_julian_day(self):
        """Converts the Julian Calendar date to its corresponding Julian Day number

        Note that the algorithm is only valid for Julian Day numbers greater than or
        equal to zero, i.e. Julian calendar years after -4712 (4713 BCE). Earlier
        calendar years will raise a ValueError.

        Adapted from: https://www.researchgate.net/publication/316558298_Date_Algorithms#pf5

        Returns:
            (int): The Julian Day number corresponding to the Julian Calendar date

        """

        if self.year < -4712:
            raise ValueError("Algorithm only valid for Julian year greater than or equal to -4712")

        if self.month < 3:
            M = self.month + 12
            Y = self.year - 1
        else:
            M = self.month
            Y = self.year

        D = self.day

        return D + (153 * M - 457) // 5 + 365 * Y + math.floor(Y / 4) + 1721116.5

    def to_gregorian(self, as_datetime=False):
        return julian_day_to_gregorian(round(self.to_julian_day()))


    def to_mayadate(self, correlation=584283):

        from LongCount import LongCount, kin_to_long_count
        from Mayadate import Mayadate

        num_kin = round(self.to_julian_day()) - correlation
        long_count = kin_to_long_count(num_kin)

        return Mayadate(long_count, None)

    def __repr__(self):
        return f"({self.day}, {self.month}, {self.year})"

    def __str__(self):
        if self.year > 0:
            return f"{_num_to_month(self.month)} {self.day}, {self.year} CE"

        elif self.year <= 0:
            return f"{_num_to_month(self.month)} {self.day}, {abs(self.year) + 1} BCE"


class GregorianDate:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def to_julian_day(self):
        """Converts a (proleptic) Gregorian calendar date to its Julian Day number equivalent

        Adapted from: https://www.researchgate.net/publication/316558298_Date_Algorithms#pf5

        Note that this function requires the astronomical year for years before 1 CE,
        i.e. 1 BCE = 0, 2 BCE = -1, etc.

        Args:
            day (int): The day of the Gregorian calendar date
            month (int): The month number of the Gregorian calendar date
            year (int): The (astronomical) year of the Gregorian calendar date

        """
        if self.month < 3:
            M = self.month + 12
            Y = self.year - 1
        else:
            M = self.month
            Y = self.year

        D = self.day

        return D + (153 * M - 457) // 5 + 365 * Y + math.floor(
            Y / 4) - math.floor(Y / 100) + math.floor(Y / 400) + 1721118.5

    def to_julian(self):
        return julian_day_to_julian(round(self.to_julian_day))

    def to_mayadate(self, correlation=584283):
        from LongCount import LongCount, kin_to_long_count
        from Mayadate import Mayadate

        num_kin = round(self.to_julian_day()) - correlation
        long_count = kin_to_long_count(num_kin)

        return Mayadate(long_count, None)

    def to_datetime(self):

        if self.year < 1:
            raise ValueError("Datetime date objects do not support years before 1 CE")

        return datetime.date(self.year, self.month, self.day)

    def __repr__(self):
        return f"({self.day}, {self.month}, {self.year})"

    def __str__(self):
        if self.year > 0:
            return f"{_num_to_month(self.month)} {self.day}, {self.year} CE"

        elif self.year <= 0:
            return f"{_num_to_month(self.month)} {self.day}, {abs(self.year) + 1} BCE"




def _convert_julian_day(julian_day, mode='julian'):
    """Converts a Julian Day number to its (proleptic) Julian or Gregorian calendar equivalent

    Adapted from: https://en.wikipedia.org/wiki/Julian_day#Julian_or_Gregorian_calendar_from_Julian_day_number

    Note that the algorithm is only valid for Julian Day numbers greater than or
    equal to zero. Negative arguments for julian_day will raise a ValueError.

    Args:
        julian_day (int): Julian Day number to convert, must be greater than or
            equal to 0
        mode (str): The target calendar to convert to, either 'julian' or
            'gregorian'. Defaults to 'julian'.

    Returns:
        A (day, month, year) tuple representing the day, month, and year in the
            target calendar.
    """
    if julian_day < 0:
        raise ValueError("Algorithm only valid for Julian Day greater than or equal to zero")
    julian_day = round(julian_day)

    # algorithm parameters
    y = 4716
    j = 1401
    m = 2
    n = 12
    r = 4
    p = 1461
    v = 3
    u = 5
    s = 153
    w = 2
    B = 274277
    C = -38

    # intermediate calculations
    if mode == 'julian':
        f = julian_day + j
    elif mode == 'gregorian':
        f = julian_day + j + (((4 * julian_day + B) // 146097) * 3) // 4 + C
    else:
        raise ValueError("Unrecognized mode - supports 'julian' or 'gregorian'")

    e = r * f + v
    g = (e % p) // r
    h = u * g + w

    day = (h % s) // u + 1  # day in target calendar
    month =  ((h // s + m) % n) + 1 # month in target calendar
    year = (e // p) - (y + (n + m - month) // n) # year in target calendar

    return day, month, year



def julian_day_to_julian(julian_day):
    """Converts a Julian Day number to its (proleptic) Julian calendar equivalent

    Adapted from: https://en.wikipedia.org/wiki/Julian_day#Julian_or_Gregorian_calendar_from_Julian_day_number

    Note that the algorithm is only valid for Julian Day numbers greater than or
    equal to zero. Negative arguments for julian_day will raise a ValueError.

    Args:
        julian_day (int): Julian Day number to convert, must be greater than or
            equal to 0

    Returns:
        A (day, month, year) tuple representing the day, month, and year in the
            Julian calendar.

    """

    day, month, year = _convert_julian_day(julian_day, mode='julian')

    return JulianDate(day, month, year)



def julian_day_to_gregorian(julian_day):
    """Converts a Julian Day number to its (proleptic) Gregorian calendar equivalent

    Adapted from: https://en.wikipedia.org/wiki/Julian_day#Julian_or_Gregorian_calendar_from_Julian_day_number

    Note that the algorithm is only valid for Julian Day numbers greater than or
    equal to zero. Negative arguments for julian_day will raise a ValueError.

    Args:
        julian_day (int): Julian Day number to convert, must be greater than or
            equal to 0

    Returns:
        A (day, month, year) tuple representing the day, month, and year in the
            Gregorian calendar.

    """
    day, month, year = _convert_julian_day(julian_day, mode='gregorian')

    return GregorianDate(day, month, year)

def datetime_to_gregorian(date):

    return GregorianDate(date.day, date.month, date.year)

def datetime_to_julian(date):

    g = GregorianDate(date.day, date.month, date.year)
    return g.to_julian()

def datetime_to_julian_day(date):

    g = GregorianDate(date.day, date.month, date.year)
    return g.to_julian_day()

def datetime_to_mayadate(date):

    g = GregorianDate(date.day, date.month, date.year)
    return g.to_mayadate()


def _num_to_month(num):

    return {1 : 'Jan',
            2 : 'Feb',
            3 : 'Mar',
            4 : 'Apr',
            5 : 'May',
            6 : 'Jun',
            7 : 'Jul',
            8 : 'Aug',
            9 : 'Sep',
            10 : 'Oct',
            11 : 'Nov',
            12 : 'Dec'}[num]
