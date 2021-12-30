from .calendar_round import CalendarRound
from .tzolkin import Tzolkin
from .haab import Haab
from .utils import julian_day_to_julian, julian_day_to_gregorian

__all__ = ["LongCount", "DistanceNumber", "kin_to_long_count"]


class LongCount:
    """Represents a position in the Maya Long Count

    Valid for dates from 0.0.0.0.0 to 19.19.19.17.19. Use NoneType to mark
    missing positions in the date for later inference.

    Attributes:
        baktun (int or NoneType): The Bak'tun number of the Long Count date.
            Integer between 0 and 19 or None.
        katun (int or NoneType): The K'atun number of the Long Count date.
            Integer between 0 and 19 or None.
        tun (int or NoneType): The Tun number of the Long Count date.
            Integer between 0 and 19 or None.
        winal (int or NoneType): The Winal number of the Long Count date.
            Integer between 0 and 17 or None.
        kin (int or NoneType): The Kin number of the Long Count date.
            Integer between 0 and 19 or None.

    """

    def __init__(self, baktun=None, katun=None, tun=None, winal=None, kin=None):
        """Creates a new LongCount object

        Use NoneType to mark missing positions in the date for later inference.

        Args:
            baktun (int or NoneType): The Bak'tun number of the Long Count date.
                Integer between 0 and 19 or None.
            katun (int or NoneType): The K'atun number of the Long Count date.
                Integer between 0 and 19 or None.
            tun (int or NoneType): The Tun number of the Long Count date.
                Integer between 0 and 19 or None.
            winal (int or NoneType): The Winal number of the Long Count date.
                Integer between 0 and 17 or None.
            kin (int or NoneType): The Kin number of the Long Count date.
                Integer between 0 and 19 or None.

        """
        if baktun is not None and baktun >= 20:
            raise ValueError("Baktun must be between 0 and 19 or NoneType")
        self.baktun = baktun
        if katun is not None and katun >= 20:
            raise ValueError("Katun must be between 0 and 19 or NoneType")
        self.katun = katun

        if tun is not None and tun >= 20:
            raise ValueError("Tun must be between 0 and 19")
        self.tun = tun

        if winal is not None and winal >= 18:
            raise ValueError("Winal must be between 0 and 17")
        self.winal = winal

        if kin is not None and kin >= 20:
            raise ValueError("Kin must be between 0 and 19")
        self.kin = kin

    def get_total_kin(self):
        """Returns the total number of kin since the initial date 0.0.0.0.0

        Returns:
            (int): The number of kin since the initial date of the Mayan calendar.

        """

        if self.has_missing():
            raise ValueError(
                "Operation not valid for incomplete Long Count dates, try inferring the missing portions"
            )

        else:
            total_kin = (
                self.kin
                + (self.winal * 20)
                + (self.tun * 20 * 18)
                + (self.katun * 18 * (20 ** 2))
                + (self.baktun * 18 * (20 ** 3))
            )

            return total_kin

    def get_calendar_round(self):
        """Returns the calendar round associated with the current LongCount object

        Returns:
            (CalendarRound): The position in the calendar round corresponding to
                the Long Count date

        """

        # Mythological start date
        initial_date = CalendarRound(Tzolkin(4, "Ajaw"), Haab(8, "Kumku"))
        initial_date.add_days(self.get_total_kin(), True)

        return initial_date

    def get_mayadate(self):
        """Returns a Mayadate object from the current LongCount object

        Returns:
            (Mayadate): The Long Count with its associated Calendar Round position

        """
        from .mayadate import Mayadate

        if self.has_missing():
            return Mayadate(self, None, None)

        return Mayadate(self, self.get_calendar_round(), None)

    def add_days(self, num_days, in_place=False):
        """Adds num_days days (kin) to the current LongCount object

        Args:
            num_days (int): The number of days to add
            in_place (bool): If True, modify the existing LongCount object, else
                return a new LongCount object. Defaults to False.

        Returns:
            (LongCount): The LongCount object num_days ahead of the current LongCount
                object's date.

        """
        total_days = self.get_total_kin() + num_days
        if in_place:
            self = kin_to_long_count(total_days)
            return self
        else:
            return kin_to_long_count(total_days)

    def get_glyph_g(self):
        """Calculates the number of the Glyph G associated with the Long Count date

        Returns:
            (str): The Glyph G associated with the given date e.g. "G6"

        """

        if self.winal is None or self.kin is None:
            raise ValueError(
                "Both the Winal and Kin numbers must be provided to infer Glyph G"
            )

        g_num = (self.winal * 20 + self.kin) % 9

        if g_num == 0:
            g_num = 9

        return f"G{g_num}"

    def to_list(self):
        """Returns a list representation of the LongCount object

        Returns:
            (list): A list of integers in the form [baktun, katun, tun, winal, kin]

        """

        return [self.baktun, self.katun, self.tun, self.winal, self.kin]

    def to_julian_day(self, correlation=584283):
        """Converts the Long Count date to its corresponding Julian Day number

        By default uses the correlation constant 584,283 proposed by Thompson.

        Args:
            correlation (int): The correlation constant to use in the conversion.
                Defaults to 584283.

        Returns:
            (int): The Julian Day number associated with the Long Count date

        """

        return self.get_total_kin() + correlation

    def to_julian(self, correlation=584283):
        """Converts the Long Count date to its corresponding Julian calendar date

        By default uses the correlation constant 584,283 proposed by Thompson.

        Args:
            correlation (int): The correlation constant to use in the conversion.
                Defaults to 584283.

        Returns:
            (JulianDate): The Julian calendar date associated with the Long Count date

        """

        julian_day = self.to_julian_day(correlation)

        return julian_day_to_julian(julian_day)

    def to_gregorian(self, correlation=584283):
        """Converts the Long Count date to its corresponding Gregorian calendar date

        By default uses the correlation constant 584,283 proposed by Thompson.

        Args:
            correlation (int): The correlation constant to use in the conversion.
                Defaults to 584283.

        Returns:
            (GregorianDate): The Gregorian calendar date associated with the Long
                Count date

        """

        julian_day = self.to_julian_day(correlation)

        return julian_day_to_gregorian(julian_day)

    def has_missing(self):
        """Checks whether the Long Count object has missing values in any position

        Returns:
            (bool): True if any of the Long Count components (baktun, katun, ...)
                are None. Otherwise returns False.

        """

        if self.baktun is None:
            return True

        if self.katun is None:
            return True

        if self.tun is None:
            return True

        if self.winal is None:
            return True

        if self.kin is None:
            return True

        return False

    def to_dict(self):
        """Returns a JSON style dictionary representation

        Returns:
            (dict): Dictionary representation of the object ready for conversion
                to JSON

        """
        return {
            "baktun": self.baktun,
            "katun": self.katun,
            "tun": self.tun,
            "winal": self.winal,
            "kin": self.kin,
        }

    def match(self, lc):
        """Checks for a potential match with another LongCount object

        A value of None is treated as matching any value, consistent with the use
        of None to mark values for later inference.

        Args:
            date (LongCount): The LongCount object to check for a match with

        Returns:
            (bool): True if the all entries match, with None as an
                automatic match. False otherwise.

        """
        baktun_match = self.__fuzzy_eq(self.baktun, lc.baktun)
        katun_match = self.__fuzzy_eq(self.katun, lc.katun)
        tun_match = self.__fuzzy_eq(self.tun, lc.tun)
        winal_match = self.__fuzzy_eq(self.winal, lc.winal)
        kin_match = self.__fuzzy_eq(self.kin, lc.kin)

        if baktun_match and katun_match and tun_match and winal_match and kin_match:
            return True
        return False

    def __fuzzy_eq(self, v1, v2):
        """Helper function for NoneType matching"""

        if v1 == v2 or v1 is None or v2 is None:
            return True

        return False

    def __add__(self, dist):

        # kin, carry = self.__add_and_carry(self.kin, dist.kin, 0, 20)
        # winal, carry = self.__add_and_carry(self.winal, dist.winal, carry, 18)
        # tun, carry = self.__add_and_carry(self.tun, dist.tun, carry, 20)
        # katun, carry = self.__add_and_carry(self.katun, dist.katun, carry, 20)
        # baktun, carry = self.__add_and_carry(self.baktun, dist.baktun, carry, 20)

        # return LongCount(baktun, katun, tun, winal, kin)

        kin_sum = self.get_total_kin() + dist.get_total_kin()
        if kin_sum >= 0:
            return kin_to_long_count(kin_sum)
        else:
            return DistanceNumber(kin_to_long_count(kin_sum * -1), sign=-1)

    # def __add_and_carry(self, val_1, val_2, carry, max):
    #     raw_sum = val_1 + val_2 + carry
    #
    #     return raw_sum % max, int(raw_sum >= max)

    def __sub__(self, dist):
        kin_diff = self.get_total_kin() - dist.get_total_kin()
        if kin_diff >= 0:
            return DistanceNumber(kin_to_long_count(kin_diff), sign=1)
        else:
            return DistanceNumber(kin_to_long_count(kin_diff * -1), sign=-1)

    def __eq__(self, date):
        if self.get_total_kin() == date.get_total_kin():
            return True
        else:
            return False

    def __gt__(self, date):
        if self.get_total_kin() > date.get_total_kin():
            return True
        else:
            return False

    def __ge__(self, date):
        if self.get_total_kin() >= date.get_total_kin():
            return True
        else:
            return False

    def __lt__(self, date):
        if self.get_total_kin() < date.get_total_kin():
            return True
        else:
            return False

    def __le__(self, date):
        if self.get_total_kin() <= date.get_total_kin():
            return True
        else:
            return False

    def __iter__(self):
        return iter(self.to_list())

    def __getitem__(self, key):
        return self.to_list().__getitem__(key)

    def __repr__(self):
        return f"{self.baktun}.{self.katun}.{self.tun}.{self.winal}.{self.kin}"


class DistanceNumber(LongCount):
    """Represents a signed Distance Number in Long Count units


    Attributes:
        long_count (LongCount): The Distance Number in Long Count units
        sign (int): 1 for a positive number, -1 for a negative number

    """

    def __init__(self, long_count=LongCount(), sign=1):
        """Creates a new DistanceNumber object


        Args:
            long_count (LongCount): The Distance Number in LongCount units
            sign (int): 1 for a positive number, -1 for a negative number

        """
        self.long_count = long_count
        super().__init__(
            long_count.baktun,
            long_count.katun,
            long_count.tun,
            long_count.winal,
            long_count.kin,
        )
        if sign == 1 or sign == -1:
            self.sign = sign
        elif sign == "+":
            self.sign = 1
        elif sign == "-":
            self.sign = -1
        else:
            raise ValueError("sign must be either 1 or -1")

    def get_total_kin(self):
        """Returns the total number of kin associated with the distance number

        Returns:
            (int): The number of kin associated with the distance number.

        """
        return self.sign * super().get_total_kin()

    def to_approx_years(self, pretty_print=False):
        total_kin = abs(self.get_total_kin())

        years = int(total_kin // 365.25)
        total_kin -= years * 365.25

        months = int(total_kin // 30.44)  # average month length
        total_kin -= months * 30.44

        if not pretty_print:
            return self.sign * years, self.sign * months, self.sign * round(total_kin)

        if self.sign == 1:
            return f"{years} years, {months} months, {round(total_kin)} days"
        else:
            return f"-{years} years, -{months} months, -{round(total_kin)} days"

    def __repr__(self):
        if self.sign == 1:
            return self.long_count.__repr__()

        else:
            return f"-{self.long_count.__repr__()}"


def kin_to_long_count(num_kin):
    """Converts the given number of days (kin) to a Long Count date

    Assumes the number of kin is counted from the Maya zero date of 0.0.0.0.0
    4 Ajaw 8 Kumk'u. For adding days to another date, use the add_days method
    of the LongCount object.

    Args:
        num_kin (int): The number of kin since the Maya zero date 0.0.0.0.0

    Returns:
        (LongCount): A Long Count date representing the position indicated by
            the given number of days after the zero date


    """

    if type(num_kin) is not int:
        num_kin = int(num_kin)

    long_count = LongCount()

    long_count.baktun = num_kin // (18 * (20 ** 3))
    num_kin = num_kin - (long_count.baktun * 18 * (20 ** 3))

    long_count.katun = num_kin // (18 * (20 ** 2))
    num_kin = num_kin - (long_count.katun * 18 * (20 ** 2))

    long_count.tun = num_kin // (18 * 20)
    num_kin = num_kin - (long_count.tun * 18 * 20)

    long_count.winal = num_kin // 20
    num_kin = num_kin - (long_count.winal * 20)

    long_count.kin = num_kin

    return long_count
