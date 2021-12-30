__all__ = ["Haab", "HAAB_MONTHS", "HAAB_IDX_TO_MONTH", "HAAB_MONTH_TO_IDX"]
# Module level constants
HAAB_MONTHS = [
    "Pop",
    "Wo",
    "Sip",
    "Sotz",
    "Sek",
    "Xul",
    "Yaxkin",
    "Mol",
    "Chen",
    "Yax",
    "Sak",
    "Keh",
    "Mak",
    "Kankin",
    "Muwan",
    "Pax",
    "Kayab",
    "Kumku",
    "Wayeb",
]

HAAB_IDX_TO_MONTH = {idx: month for idx, month in enumerate(HAAB_MONTHS)}
HAAB_MONTH_TO_IDX = {month: idx for idx, month in HAAB_IDX_TO_MONTH.items()}


class Haab:
    """Represents a month number, month name combination in the 365 day count

    Attributes:
        day_number (int): The day number associated with the Haab date
        day_name (str): The day name associated with the Haab date

    """

    def __init__(self, month_number=None, month_name=None):
        """Creates a new Haab object

        Can either be constructed from a day name, day number combination or
        from the position in the tzolkin count counting from 1 Imix.

        Args:
            month_number (int): Integer from 0-19 (or 0-4 for Wayeb)
                representing the month number
            month_name (str): month name


        """

        if month_name not in HAAB_MONTHS and month_name is not None:
            raise ValueError(f"Invalid Haab month name {month_name}")
        self.month_name = month_name

        if month_name == "Wayeb":
            if month_number not in list(range(5)):
                raise ValueError(
                    "Invalid Haab month number, Wayeb number must be between 0 and 4"
                )
        elif month_number not in list(range(20)) and month_number is not None:
            raise ValueError(
                "Invalid Haab month number, must be an integer between 0 and 19 or NoneType"
            )

        self.month_number = month_number

        if not self.has_missing():
            self.haab_num = 20 * HAAB_MONTH_TO_IDX[month_name] + month_number
        else:
            self.haab_num = None

    def has_missing(self):
        """Checks whether the month number or name is missing

        Returns:
            (bool): True if either the month number or month name is None, False
                otherwise

        """
        if self.month_name is None or self.month_number is None:
            return True

        return False

    def reset_by_haab_num(self, new_num):
        """Set the Haab object to a new position by its 365 day count number

        Note:
            0 Pop is used as the reference 'Day 0' of the cycle

        Args:
            new_num (int): Integer from 0-365 representing new position in the
                365 day count.
        """
        self.month_name = HAAB_IDX_TO_MONTH[new_num // 20]
        self.month_number = new_num % 20

        return self

    def add_days(self, num_days, in_place=False):
        """Adds days to the current Haab object

        Args:
            num_days (int): Number of days to add to the Haab object
            in_place (bool): Whether to modify the existing object or return a
                new object. Defaults to False.

        Returns:
            A new Haab object num_days ahead of the previous object

        """
        new_num = (self.haab_num + num_days) % 365
        if in_place:
            self.haab_num = new_num
            self.reset_by_haab_num(self.haab_num)

            return self
        else:
            return Haab().reset_by_haab_num(new_num)

    def match(self, date):
        """Checks for a potential match with another Haab object

        A value of None is treated as matching any value, consistent with the use
        of None to mark values for later inference.

        Args:
            date (Haab): The Haab object to check for a match with

        Returns:
            (bool): True if the month name and number match, with None as an
                automatic match. False otherwise.

        """

        name_same = self.__fuzzy_eq(self.month_name, date.month_name)
        num_same = self.__fuzzy_eq(self.month_number, date.month_number)

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
        return {"month_number": self.month_number, "month_name": self.month_name}

    def __fuzzy_eq(self, v1, v2):
        """Helper function for NoneType matching"""

        if v1 == v2 or v1 is None or v2 is None:
            return True

        return False

    def __eq__(self, date):
        name_same = self.month_name == date.month_name
        num_same = self.month_number == date.month_number

        if name_same and num_same:
            return True
        else:
            return False

    def __sub__(self, date):
        return abs(self.haab_num - date.haab_num)

    def __repr__(self):
        return f"{self.month_number} {self.month_name}"
