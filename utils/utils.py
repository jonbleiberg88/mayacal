

class JulianDate:

    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def to_julian_day(self):
    """

    Adapted from: https://en.wikipedia.org/wiki/Julian_day#Converting_Julian_calendar_date_to_Julian_Day_Number

    """
        if self.year < -4712:
            raise ValueError("Algorithm only valid for Julian year greater than or equal to -4712")

        return 367 × self.year − (7 × (self.year + 5001 + (self.month − 9)/7))/4 +
            (275 × self.month)/9 + self.day + 1729777

    def to_gregorian(self):
        return julian_day_to_gregorian(self.to_julian_day())



    def to_mayadate(self, correlation):
        return 

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
    return _convert_julian_day(julian_day, mode='julian')



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
    return _convert_julian_day(julian_day, mode='gregorian')

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
