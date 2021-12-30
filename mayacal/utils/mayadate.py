from .calendar_round import CalendarRound
from .long_count import LongCount
from .tzolkin import Tzolkin
from .haab import Haab
from .utils import *
import logging

__all__ = ["Mayadate", "from_dict"]


class Mayadate:
    """Umbrella class to handle Maya calendar dates, conversions, and inference

    Attributes:
        long_count (LongCount): The Long Count representation of the date
        calendar_round (CalendarRound): The Calendar Round position of the date
        glyph_g (str): The Glyph G associated with the date

    """

    def __init__(self, long_count=None, calendar_round=None, glyph_g=None):
        """Creates a new Mayadate object

        Args:
            long_count (LongCount): The Long Count representation of the date
            calendar_round (CalendarRound): The Calendar Round position of the
                date
            glyph_g (str): The Glyph G associated with the date, e.g. "G3"

        """
        if long_count is None:
            self.long_count = LongCount(None, None, None, None, None)
            self.glyph_g = glyph_g
        else:
            self.long_count = long_count
            if long_count.winal is not None and long_count.kin is not None:
                g = self.long_count.get_glyph_g()
                if g != glyph_g and glyph_g is not None:
                    raise ValueError(
                        "Provided Glyph G does not match the Long Count date"
                    )
                self.glyph_g = g

            else:
                self.glyph_g = glyph_g

        if calendar_round is None:
            if long_count is not None:
                if not self.long_count.has_missing():
                    self.calendar_round = self.long_count.get_calendar_round()
                else:
                    self.calendar_round = CalendarRound(None, None)
        else:
            self.calendar_round = calendar_round

    def has_missing(self):
        """Checks whether the Mayadate object has missing values in any position

        Returns:
            (bool): True if any of the Long Count components (baktun, katun, ...)
                or Calendar Round components are None. Otherwise returns False.

        """
        return self.long_count.has_missing() or self.calendar_round.has_missing()

    def add_days(self, num_days, in_place=False):
        """Adds num_days days (kin) to the current Mayadate object

        Args:
            num_days (int): The number of days to add
            in_place (bool): If True, modify the existing Mayadate object, else
                return a new Mayadate object. Defaults to False.

        Returns:
            (Mayadate): The Mayadate object num_days ahead of the current Mayadate
                object's date.

        """

        if in_place:
            self.long_count = self.long_count.add_days(num_days)
            self.calendar_round = self.calendar_round.add_days(num_days)

            return self
        else:
            return Mayadate(
                self.long_count.add_days(num_days),
                self.calendar_round.add_days(num_days),
            )

    def infer_long_count_dates(self):
        """Finds Long Count dates that match the supplied information

        Returns:
            (list) A list of potential Long Count dates that match the supplied
                portions of the Long Count and Calendar Round Dates

        """

        if not self.long_count.has_missing():
            return [self.long_count]

        if not self.calendar_round.has_missing():
            min_lc, max_lc = LongCount(0, 0, 0, 0, 0), LongCount(13, 19, 19, 17, 19)
            poss_lc = self.calendar_round.get_long_count_possibilities(min_lc, max_lc)
            poss_lc = [lc for lc in poss_lc if self.match(lc.get_mayadate())]

        else:
            poss_lc = self.__infer_lc_recursive(self.long_count.to_list(), [])

        if poss_lc == []:
            logging.info("No matching dates found - check the inputted values")

        return poss_lc

    def infer_mayadates(self):
        """Finds Maya calendar dates that match the supplied information

        Returns:
            (list) A list of potential Mayadate objects that match the supplied
                portions of the Long Count and Calendar Round Dates

        """
        if not self.long_count.has_missing():
            return [self.long_count.get_mayadate()]

        lcs = self.infer_long_count_dates()
        if lcs == []:
            logging.info("No matching dates found - check the inputted values")
        return [lc.get_mayadate() for lc in lcs]

    def __infer_lc_recursive(self, lc, poss_dates):
        """Helper function to recursively check for possible dates"""

        if None not in lc:
            lc_obj = LongCount(*lc)
            if self.calendar_round.match(lc_obj.get_calendar_round()):
                if self.glyph_g is not None:
                    if lc_obj.get_glyph_g() == self.glyph_g:
                        return lc_obj
                else:
                    return lc_obj
            return

        max_vals = [14, 20, 20, 18, 20]

        for idx, v in enumerate(zip(lc, max_vals)):
            val, max = v
            if val is None:
                for i in range(max):

                    lc_test = lc[:]
                    lc_test[idx] = i

                    res = self.__infer_lc_recursive(lc_test, poss_dates)
                    if type(res) is LongCount:
                        poss_dates.append(res)
                break

        return poss_dates

    def to_julian_day(self, correlation=584283):
        """Converts the Mayan calendar date to its corresponding Julian Day number

        By default uses the correlation constant 584,283 proposed by Thompson.

        Args:
            correlation (int): The correlation constant to use in the conversion.
                Defaults to 584283.

        Returns:
            (int): The Julian Day number associated with the Mayan calendar date

        """
        return self.long_count.to_julian_day(correlation)

    def to_julian(self, correlation=584283):
        """Converts the Mayan calendar date to its corresponding Julian calendar date

        By default uses the correlation constant 584,283 proposed by Thompson.

        Args:
            correlation (int): The correlation constant to use in the conversion.
                Defaults to 584283.

        Returns:
            (JulianDate): The Julian calendar date associated with the Mayan
                calendar date

        """
        return self.long_count.to_julian(correlation)

    def to_gregorian(self, correlation=584283):
        """Converts the Mayan calendar date to its corresponding Gregorian calendar date

        By default uses the correlation constant 584,283 proposed by Thompson.

        Args:
            correlation (int): The correlation constant to use in the conversion.
                Defaults to 584283.

        Returns:
            (int): The Gregorian calendar date associated with the Mayan
                calendar date

        """
        return self.long_count.to_gregorian(correlation)

    def get_total_kin(self):
        """Returns the total number of kin since the initial date 0.0.0.0.0

        Returns:
            (int): The number of kin since the initial date of the Mayan calendar.

        """
        return self.long_count.get_total_kin()

    def get_glyph_g(self):
        """Calculates the number of the Glyph G associated with the Long Count date

        Returns:
            (str): The Glyph G associated with the given date e.g. "G6"

        """

        return self.long_count.get_glyph_g()

    def to_dict(self):
        """Returns a JSON style dictionary representation

        Output dictionary will be in format:
        {
            'long_count' : {
                'baktun' : 9,
                'katun' : 0,
                'tun' : 0,
                'winal' : 0,
                'kin' : 0
            },

            'calendar_round' : {
                'tzolkin' : {
                    'day_number' : 8,
                    'day_name' : "Ajaw"
                },
                'haab' : {
                    'month_number' : 13,
                    'month_name' : "Keh"
                }
            },
            'glyph_g' : 'G9'
        }
        Missing values will be replaced with None.

        Returns:
            (dict): Dictionary representation of the object ready for conversion
                to JSON

        """
        date_dict = {
            "long_count": self.long_count.to_dict(),
            "calendar_round": self.calendar_round.to_dict(),
            "glyph_g": self.glyph_g,
        }
        return date_dict

    def match(self, date):
        """Checks for a potential match with another Mayadate object

        A value of None is treated as matching any value, consistent with the use
        of None to mark values for later inference.

        Args:
            date (Mayadate): The Mayadate object to check for a match with

        Returns:
            (bool): True if the all entries match, with None as an
                automatic match. False otherwise.

        """
        lc_match = self.long_count.match(date.long_count)
        cr_match = self.calendar_round.match(date.calendar_round)
        g_match = self.__fuzzy_eq(self.glyph_g, date.glyph_g)

        if lc_match and cr_match and g_match:
            return True
        return False

    def __fuzzy_eq(self, v1, v2):
        """Helper function for NoneType matching"""

        if v1 == v2 or v1 is None or v2 is None:
            return True

        return False

    def __add__(self, dist):
        lc = self.long_count + dist.long_count

        return lc.get_mayadate()

    def __sub__(self, dist):
        dist = self.long_count - dist.long_count

        return dist

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

    def __repr__(self):
        return f"{self.long_count.__repr__()}  {self.calendar_round.__repr__()}"


def from_dict(dict_obj):
    """Converts dictionary to Mayadate object

    Mainly intended for use with JSON objects.
    Dictionary must be in format:
        {
            'long_count' : {
                'baktun' : 9,
                'katun' : 0,
                'tun' : 0,
                'winal' : 0,
                'kin' : 0
            },

            'calendar_round' : {
                'tzolkin' : {
                    'day_number' : 8,
                    'day_name' : "Ajaw"
                },
                'haab' : {
                    'month_number' : 13,
                    'month_name' : "Keh"
                }
            },
            'glyph_g' : 'G9'
        }
    Missing values should be replaced with None.

    Args:
        dict_obj (dict): Dictionary in above format to convert

    Returns:
        (Mayadate): the corresponding Mayadate object
    """
    lc_dict = _none_to_dict(dict_obj.get("long_count", {}))

    cr_dict = _none_to_dict(dict_obj.get("calendar_round", {}))

    tz_dict = _none_to_dict(cr_dict.get("tzolkin", {}))
    hb_dict = _none_to_dict(cr_dict.get("haab", {}))

    glyph_g = dict_obj.get("glyph_g")

    return Mayadate(
        long_count=LongCount(**lc_dict),
        calendar_round=CalendarRound(Tzolkin(**tz_dict), Haab(**hb_dict)),
        glyph_g=glyph_g,
    )


def _none_to_dict(obj):
    if type(obj) is dict:
        return obj
    elif obj is None:
        return {}
    else:
        raise ValueError("Dictionary not properly formatted - see documentation")


def main():
    pass


if __name__ == "__main__":
    main()
