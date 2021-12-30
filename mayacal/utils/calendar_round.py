from .haab import Haab
from .tzolkin import Tzolkin, TZOLKIN_DAY_TO_NUM

__all__ = ["CalendarRound"]


class CalendarRound:
    """Represents a position in the Mayan Calendar Round.

    Supports use of NoneType to mark positions for later inference.

    Attributes:
        tzolkin (Tzolkin): The tzolkin date portion of the the Calendar Round position
        haab (Haab): The haab date portion of the the Calendar Round position
        valid (bool): Whether the Tzolkin day name matches the Haab month number

    """

    def __init__(self, tzolkin=None, haab=None, override_coef_check=False):
        """Creates a new CalendarRound object

        Supports use of NoneType to mark positions for later inference.

        Note that each Tzolkin day name can only occur with a specific set of Haab
        month coefficients. Throws a ValueError if these rules are violated. Can
        override these rules (for example for work with Post Classic dates) by
        setting override_coef_check to True.

        Args:
            tzolkin (Tzolkin or NoneType): The tzolkin date portion of the the
                Calendar Round position. Use None to denote missing Tzolkin date.
            haab (Haab or NoneType): The haab date portion of the the Calendar
                Round position. Use None to denote missing Haab date.
            override_coef_check (bool): Whether to override the check for valid
                month number, day name combinations. Defaults to False.

        """

        if tzolkin is None:
            self.tzolkin = Tzolkin(None, None)
        else:
            self.tzolkin = tzolkin

        if haab is None:
            self.haab = Haab(None, None)
        else:
            self.haab = haab

        self.valid = self.__check_valid()

        if not override_coef_check and not self.valid:
            raise ValueError("Invalid Haab month coefficient, Tzolkin day name combo")

    def has_missing(self):
        """Checks whether the Calendar Round has any missing components

        Returns:
            (bool): True if the Tzolkin or Haab contain missing components.
                False otherwise.

        """

        return self.tzolkin.has_missing() or self.haab.has_missing()

    def add_days(self, num_days, in_place=False):
        """Adds num_days days (kin) to the current CalendarRound object

        Args:
            num_days (int): The number of days to add
            in_place (bool): If True, modify the existing CalendarRound object,
                else return a new CalendarRound object. Defaults to False.

        Returns:
            (CalendarRound): The CalendarRound object num_days ahead of the current
                CalendarRound object's date.

        """
        if in_place:
            self.haab.add_days(num_days, True)
            self.tzolkin.add_days(num_days, True)

            return self

        else:
            new_haab = self.haab.add_days(num_days)
            new_tzolkin = self.tzolkin.add_days(num_days)

            return CalendarRound(new_tzolkin, new_haab)

    def __check_valid(self):
        """Checks whether the Tzolkin day name can occur with the Haab month number

        Returns:
            (bool): True if the Tzolkin day name can occur with the Haab month
                number. False otherwise.

        """

        if self.haab.month_number is None or self.tzolkin.day_name is None:
            return True

        if self.haab.month_number % 5 == 0:
            if self.tzolkin.day_name not in ("Kaban", "Ik", "Manik", "Eb"):
                return False

            return True

        elif self.haab.month_number % 5 == 1:
            if self.tzolkin.day_name not in ("Etznab", "Akbal", "Lamat", "Ben"):
                return False
            return True

        elif self.haab.month_number % 5 == 2:
            if self.tzolkin.day_name not in ("Kawak", "Kan", "Muluk", "Ix"):
                return False
            return True

        elif self.haab.month_number % 5 == 3:
            if self.tzolkin.day_name not in ("Ajaw", "Chikchan", "Ok", "Men"):
                return False
            return True

        elif self.haab.month_number % 5 == 4:
            if self.tzolkin.day_name not in ("Imix", "Kimi", "Chuwen", "Kib"):
                return False
            return True

        else:
            raise ValueError(f"Invalid month coefficient {self.haab.month_number}")

    def get_long_count_possibilities(self, min_date, max_date):
        """Finds Long Count dates that correspond to the Calendar Round date

        Finds all Long Count dates that correspond to the Calendar Round date
        between min_date and max_date. Note that the Calendar Round cycle repeats
        every 18,980 days, i.e. the LCM of the 260 day Tzolkin cycle and the 365
        day Haab cycle.

        Args:
            min_date (LongCount): The earliest Long Count date to check
            max_date (LongCount): The latest Long Count date to check

        Returns:
            (list): A list of LongCount objects representing the possible dates

        """
        from .long_count import LongCount, kin_to_long_count

        min_cal_round = min_date.get_calendar_round()
        init_num = TZOLKIN_DAY_TO_NUM[
            (min_cal_round.tzolkin.day_number, min_cal_round.tzolkin.day_name)
        ]
        day_num = TZOLKIN_DAY_TO_NUM[(self.tzolkin.day_number, self.tzolkin.day_name)]

        cycle_num = (day_num - init_num) % 260

        lc = min_date.add_days(cycle_num)

        count = 0
        while True:
            if lc.get_calendar_round().haab == self.haab:
                break
            count += 1
            lc = lc.add_days(260)

        poss_dates = []

        while True:
            if lc > max_date:
                return poss_dates

            poss_dates.append(lc)
            lc = lc.add_days(18980)  # LCM of 260 and 365

    def to_dict(self):
        """Returns a JSON style dictionary representation

        Returns:
            (dict): Dictionary representation of the object ready for conversion
                to JSON

        """
        return {"tzolkin": self.tzolkin.to_dict(), "haab": self.haab.to_dict()}

    def match(self, date):
        """Checks for a potential match with another CalendarRound object

        A value of None is treated as matching any value, consistent with the use
        of None to mark values for later inference.

        Args:
            date (CalendarRound): The CalendarRound object to check for a match with

        Returns:
            (bool): True if the Tzolkin and Haab match, with None as an
                automatic match. False otherwise.

        """

        if self.tzolkin.match(date.tzolkin) and self.haab.match(date.haab):
            return True

        else:
            return False

    def __eq__(self, date):
        if self.tzolkin == date.tzolkin and self.haab == date.haab:
            return True
        else:
            return False

    def __repr__(self):
        return f"{self.tzolkin.__repr__()} {self.haab.__repr__()}"
