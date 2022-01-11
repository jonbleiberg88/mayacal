import math
import datetime

__all__ = [
    "JulianDate",
    "GregorianDate",
    "julian_day_to_julian",
    "julian_day_to_gregorian",
    "datetime_to_gregorian",
    "datetime_to_julian",
    "datetime_to_julian_day",
    "datetime_to_mayadate",
]


class JulianDate:
    """Basic class to handle (proleptic) Julian calendar dates and conversions

    Note that this class uses the astronomical year convention for years before 1 CE,
    i.e. 1 BCE = 0, 2 BCE = -1, etc.

    Attributes:
        day (int): The day of the Julian calendar date
        month (int): The month number of the Julian calendar date
        year (int): The (astronomical) year number of the Julian calendar date
    """

    def __init__(self, day, month, year):
        """Creates a new JulianDate object

        Note that this class uses the astronomical year convention for years before 1 CE,
        i.e. 1 BCE = 0, 2 BCE = -1, etc.

        Args:
            day (int): The day of the Julian calendar date
            month (int): The month number of the Julian calendar date
            year (int): The (astronomical) year number of the Julian calendar date
        """
        if day > 31 or day < 1:
            raise ValueError("Invalid day, must be integer between 1 and 31")
        self.day = day

        if month > 12 or month < 1:
            raise ValueError("Invalid month, must be integer between 1 and 12")
        self.month = month

        self.year = year

        self.__check_month_days()

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
            raise ValueError(
                "Algorithm only valid for Julian year greater than or equal to -4712"
            )

        if self.month < 3:
            M = self.month + 12
            Y = self.year - 1
        else:
            M = self.month
            Y = self.year

        D = self.day

        return D + (153 * M - 457) // 5 + 365 * Y + math.floor(Y / 4) + 1721116.5

    def to_gregorian(self, as_datetime=False):
        """Converts the Julian calendar date to its Gregorian calendar equivalent

        Returns:
            (GregorianDate): The Gregorian calendar date corresponding to the
                Julian calendar date.

        """
        return julian_day_to_gregorian(round(self.to_julian_day()))

    def to_mayadate(self, correlation=584283):
        """Converts the Julian calendar date to its Mayan calendar equivalent

        Returns:
            (Mayadate): The Mayan calendar date corresponding to the Gregorian
                calendar date.

        """

        from .long_count import LongCount, kin_to_long_count
        from .mayadate import Mayadate

        num_kin = round(self.to_julian_day()) - correlation
        long_count = kin_to_long_count(num_kin)

        return Mayadate(long_count, None)

    def is_leap_year(self):
        """Determines whether the year of the JulianDate object is a leap year

        Returns:
            (bool): True if the year is a leap year, False otherwise

        """
        if self.year % 4 == 0:
            return True

        return False

    def __check_month_days(self):
        """Raises error if the current configuration of month, day, year is invalid"""

        max_days = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }

        if self.is_leap_year():
            max_days[2] = 29

        if max_days[self.month] < self.day:
            raise ValueError(f"Invalid day, month combination {self.month}/{self.day}")

    def __eq__(self, other):
        return (
            self.day == other.day
            and self.month == other.month
            and self.year == other.year
        )

    def __repr__(self):
        return f"({self.day}, {self.month}, {self.year})"

    def __str__(self):
        if self.year > 0:
            return f"{_num_to_month(self.month)} {self.day}, {self.year} CE"

        elif self.year <= 0:
            return f"{_num_to_month(self.month)} {self.day}, {abs(self.year) + 1} BCE"


class GregorianDate:
    """Basic class to handle (proleptic) Gregorian calendar dates and conversions

    Note that this class uses the astronomical year convention for years before 1 CE,
    i.e. 1 BCE = 0, 2 BCE = -1, etc.

    Attributes:
        day (int): The day of the Gregorian calendar date
        month (int): The month number of the Gregorian calendar date
        year (int): The (astronomical) year number of the Gregorian calendar date
    """

    def __init__(self, day, month, year):
        """Creates a new GregorianDate object

        Note that this class uses the astronomical year convention for years before 1 CE,
        i.e. 1 BCE = 0, 2 BCE = -1, etc.

        Args:
            day (int): The day of the Gregorian calendar date
            month (int): The month number of the Gregorian calendar date
            year (int): The (astronomical) year number of the Gregorian calendar date
        """
        if day > 31 or day < 1:
            raise ValueError("Invalid day, must be integer between 1 and 31")
        self.day = day

        if month > 12 or month < 1:
            raise ValueError("Invalid month, must be integer between 1 and 12")
        self.month = month

        self.year = year

        self.__check_month_days()

    def to_julian_day(self):
        """Converts the Gregorian calendar date to its Julian Day number equivalent

        Adapted from: https://www.researchgate.net/publication/316558298_Date_Algorithms#pf5

        Returns:
            (float): The Julian day number corresponding to the Gregorian calendar
                date.

        """
        if self.month < 3:
            M = self.month + 12
            Y = self.year - 1
        else:
            M = self.month
            Y = self.year

        D = self.day

        return (
            D
            + (153 * M - 457) // 5
            + 365 * Y
            + math.floor(Y / 4)
            - math.floor(Y / 100)
            + math.floor(Y / 400)
            + 1721118.5
        )

    def to_julian(self):
        """Converts the Gregorian calendar date to its Julian calendar equivalent

        Returns:
            (JulianDate): The Julian calendar date corresponding to the Gregorian
                calendar date.

        """
        return julian_day_to_julian(round(self.to_julian_day))

    def to_mayadate(self, correlation=584283):
        """Converts the Gregorian calendar date to its Mayan calendar equivalent

        Returns:
            (Mayadate): The Mayan calendar date corresponding to the Gregorian
                calendar date.

        """
        from .long_count import LongCount, kin_to_long_count
        from .mayadate import Mayadate

        num_kin = round(self.to_julian_day()) - correlation
        long_count = kin_to_long_count(num_kin)

        return Mayadate(long_count, None)

    def to_datetime(self):
        """Converts the GregorianDate object to a datetime.date object

        Note that datetime.date objects do not support years before 1 CE. Attempting
        to convert GregorianDate objects with year before 1 CE will raise a ValueError.

        Returns:
            (datetime.date): The datetime.date object corresponding to the Gregorian
                calendar date.

        """
        if self.year < 1:
            raise ValueError("datetime.date objects do not support years before 1 CE")

        return datetime.date(self.year, self.month, self.day)

    def is_leap_year(self):
        """Determines whether the year of the GregorianDate object is a leap year

        Returns:
            (bool): True if the year is a leap year, False otherwise

        """
        if self.year % 4 == 0:
            if self.year % 100 == 0 and self.year % 400 != 0:
                return False
            else:
                return True

        return False

    def __check_month_days(self):
        """Raises error if the current configuration of month, day, year is invalid"""
        max_days = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }

        if self.is_leap_year():
            max_days[2] = 29

        if max_days[self.month] < self.day:
            raise ValueError(f"Invalid day, month combination {self.month}/{self.day}")

    def __eq__(self, other):
        return (
            self.day == other.day
            and self.month == other.month
            and self.year == other.year
        )

    def __repr__(self):
        return f"({self.day}, {self.month}, {self.year})"

    def __str__(self):
        if self.year > 0:
            return f"{_num_to_month(self.month)} {self.day}, {self.year} CE"

        elif self.year <= 0:
            return f"{_num_to_month(self.month)} {self.day}, {abs(self.year) + 1} BCE"


def _convert_julian_day(julian_day, mode="julian"):
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
        raise ValueError(
            "Algorithm only valid for Julian Day greater than or equal to zero"
        )
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
    if mode == "julian":
        f = julian_day + j
    elif mode == "gregorian":
        f = julian_day + j + (((4 * julian_day + B) // 146097) * 3) // 4 + C
    else:
        raise ValueError("Unrecognized mode - supports 'julian' or 'gregorian'")

    e = r * f + v
    g = (e % p) // r
    h = u * g + w

    day = (h % s) // u + 1  # day in target calendar
    month = ((h // s + m) % n) + 1  # month in target calendar
    year = (e // p) - y + ((n + m - month) // n)  # year in target calendar

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

    day, month, year = _convert_julian_day(julian_day, mode="julian")

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
    day, month, year = _convert_julian_day(julian_day, mode="gregorian")

    return GregorianDate(day, month, year)


def datetime_to_gregorian(date):
    """Converts a datetime.date object to a GregorianDate object

    Args:
        date (datetime.date): The datetime.date object to convert

    Returns:
        (GregorianDate): The corresponding GregorianDate object

    """

    return GregorianDate(date.day, date.month, date.year)


def datetime_to_julian(date):
    """Converts a datetime.date object to the corresponding Julian calendar date

    Args:
        date (datetime.date): The datetime.date object to convert

    Returns:
        (JulianDate): The corresponding Julian calendar date

    """

    g = GregorianDate(date.day, date.month, date.year)
    return g.to_julian()


def datetime_to_julian_day(date):
    """Converts a datetime.date object to the corresponding Julian Day number

    Args:
        date (datetime.date): The datetime.date object to convert

    Returns:
        (float): The corresponding Julian Day number

    """

    g = GregorianDate(date.day, date.month, date.year)
    return g.to_julian_day()


def datetime_to_mayadate(date):
    """Converts a datetime.date object to the corresponding Maya calendar date

    Args:
        date (datetime.date): The datetime.date object to convert

    Returns:
        (Mayadate): The corresponding Mayan calendar date.

    """

    g = GregorianDate(date.day, date.month, date.year)
    return g.to_mayadate()


def _num_to_month(num):
    """Helper function to convert month number to short name

    Args:
        num (int): the month number to convert

    Returns:
        (str): The three letter short name of the corresponding month

    """

    return {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }[num]
