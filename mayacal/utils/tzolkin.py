__all__ = [
    "Tzolkin",
    "TZOLKIN_DAYS",
    "TZOLKIN_DAY_TO_NUM",
    "TZOLKIN_IDX_TO_DAY",
    "TZOLKIN_NUM_TO_DAY",
    "TZOLKIN_DAY_TO_IDX",
]
# Module level constants
TZOLKIN_DAYS = [
    "Imix",
    "Ik",
    "Akbal",
    "Kan",
    "Chikchan",
    "Kimi",
    "Manik",
    "Lamat",
    "Muluk",
    "Ok",
    "Chuwen",
    "Eb",
    "Ben",
    "Ix",
    "Men",
    "Kib",
    "Kaban",
    "Etznab",
    "Kawak",
    "Ajaw",
]

TZOLKIN_IDX_TO_DAY = {idx: day for idx, day in enumerate(TZOLKIN_DAYS)}
TZOLKIN_DAY_TO_IDX = {day: idx for idx, day in TZOLKIN_IDX_TO_DAY.items()}

TZOLKIN_NUM_TO_DAY = {}

for _i in range(260):
    _date = ((_i % 13) + 1, TZOLKIN_IDX_TO_DAY[(_i % 20)])
    TZOLKIN_NUM_TO_DAY[_i] = _date

TZOLKIN_DAY_TO_NUM = {date: num for num, date in TZOLKIN_NUM_TO_DAY.items()}


class Tzolkin:
    """Represents a day number, day name combination in the 260 day count

    Attributes:
        day_number (int): The day number associated with the Tzolkin date
        day_name (str): The day name associated with the Tzolkin date
        tzolkin_num (int): Integer from 0-259 representing days since 1 Imix.

    """

    def __init__(self, day_number=None, day_name=None, tzolkin_num=None):
        """Creates a new Tzolkin object

        Can either be constructed from a day name, day number combination or
        from the position in the tzolkin count counting from 1 Imix.

        Args:
            day_number (int): Integer from 1-13 representing the day number
            day_name (str): Day name


        """

        if tzolkin_num is not None:
            # check if day name/number matches tzolkin number if provided
            if day_number is not None and day_name is not None:
                implied_num = TZOLKIN_DAY_TO_NUM[(day_number, day_name)]
                if implied_num != tzolkin_num:
                    raise ValueError(
                        f"Provided Tzolkin number {tzolkin_num} does not match provided day name and number {day_number} {day_name}"
                    )

            self.reset_by_tzolkin_num(tzolkin_num)

        else:
            if day_name not in TZOLKIN_DAYS and day_name is not None:
                raise ValueError(f"Invalid tzolkin day name {day_name}")
            self.day_name = day_name

            if day_number not in list(range(1, 14)) and day_number is not None:
                raise ValueError(
                    "Invalid tzolkin day number - must be integer between 1 and 13"
                )
            self.day_number = day_number

            if day_number is not None and day_name is not None:
                self.tzolkin_num = TZOLKIN_DAY_TO_NUM[(day_number, day_name)]

    def reset_by_tzolkin_num(self, new_num):
        """Set the Tzolkin object to a new position by its 260 day count number

        Note:
            1 Imix is used as the reference 'Day 0' of the cycle

        Args:
            new_num (int): Integer from 0-259 representing new position in the
                260 day count.
        """

        if new_num >= 260:
            raise ValueError("Invalid Tzolkin number, must be between 0 and 259")

        self.tzolkin_num = new_num
        self.day_number, self.day_name = TZOLKIN_NUM_TO_DAY[self.tzolkin_num]

    def add_days(self, num_days, in_place=False):
        """Adds days to the current Tzolkin object

        Args:
            num_days (int): Number of days to add to the Tzolkin object
            in_place (bool): Whether to modify the existing object or return a
                new object. Defaults to False.

        Returns:
            A new Tzolkin object num_days ahead of the previous object

        """
        new_num = (self.tzolkin_num + num_days) % 260
        if in_place:
            self.reset_by_tzolkin_num(new_num)
            return self

        else:
            return Tzolkin(tzolkin_num=new_num)

    def has_missing(self):
        """Checks whether the day number or name is missing

        Returns:
            (bool): True if either the day number or day name is None, False
                otherwise

        """
        if self.day_name is None or self.day_number is None:
            return True

        return False

    def match(self, date):
        """Checks for a potential match with another Tzolkin object

        A value of None is treated as matching any value, consistent with the use
        of None to mark values for later inference.

        Args:
            date (Tzolkin): The Tzolkin object to check for a match with

        Returns:
            (bool): True if the day name and number match, with None as an
                automatic match. False otherwise.

        """
        name_same = self.__fuzzy_eq(self.day_name, date.day_name)
        num_same = self.__fuzzy_eq(self.day_number, date.day_number)

        if name_same and num_same:
            return True

        else:
            return False

    def to_dict(self):
        """Returns a JSON style dictionary representation

        Returns:
            (dict): Dictionary representation of the object ready for conversion
                to JSON

        """
        return {"day_number": self.day_number, "day_name": self.day_name}

    def __fuzzy_eq(self, v1, v2):
        """Helper function for NoneType matching"""

        if v1 == v2 or v1 is None or v2 is None:
            return True

        return False

    def __eq__(self, date):
        name_same = self.day_name == date.day_name
        num_same = self.day_number == date.day_number

        if name_same and num_same:
            return True

        else:
            return False

    def __sub__(self, date):
        return abs(self.tzolkin_num - date.tzolkin_num)

    def __repr__(self):
        return f"{self.day_number} {self.day_name}"
