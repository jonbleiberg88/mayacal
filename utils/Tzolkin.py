
tzolkin_days = ["Imix", "Ik", "Akbal", "Kan", "Chikchan", "Kimi", "Manik",
                    "Lamat", "Muluk", "Ok", "Chuwen", "Eb", "Ben", "Ix",
                    "Men", "Kib", "Kaban", "Etznab", "Kawak", "Ajaw"]

tzolkin_idx_to_day = {idx:day for idx, day in enumerate(tzolkin_days)}
tzolkin_day_to_idx = {day:idx for idx, day in tzolkin_idx_to_day.items()}

tzolkin_num_to_day = {}
for i in range(260):
    date = ((i % 13) + 1, tzolkin_idx_to_day[(i % 20)])
    tzolkin_num_to_day[i] = date

tzolkin_day_to_num = {date:num for num, date in tzolkin_num_to_day.items()}

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
                implied_num = tzolkin_day_to_num[(day_number, day_name)]
                if implied_num != tzolkin_num:
                    raise ValueError(f"Provided Tzolkin number {tzolkin_num} does not match provided day name and number {day_number} {day_name}")

            self.reset_by_tzolkin_num(self, tzolkin_num)

        else:
            if day_name not in tzolkin_days:
                raise ValueError(f"Invalid tzolkin day name {day_name}")
            self.day_name = day_name

            if day_number not in list(range(1, 13)):
                raise ValueError("Invalid tzolkin day number - must be integer between 1 and 13")
            self.day_number = day_number

            self.tzolkin_num = tzolkin_day_to_num[(day_number, day_name)]

    def reset_by_tzolkin_num(self, new_num):
        """ Set the Tzolkin object to a new position by its 260 day count number

        Note:
            1 Imix is used as the reference 'Day 0' of the cycle

        Args:
            new_num (int): Integer from 0-259 representing new position in the
                260 day count.
        """

        if new_num >= 260:
            raise ValueError("Invalid Tzolkin number, must be between 0 and 259")

        self.tzolkin_num = new_num
        self.day_number, self.day_name = tzolkin_num_to_day[self.tzolkin_num]

    def add_days(self, num_days):
        """ Adds days to the current Tzolkin object

        """
        new_num = (self.tzolkin_num + num_days) % 260
        self.reset_by_tzolkin_num(new_num)

        return self

    def match(self, date):
        name_same = self.__fuzzy_eq(self.day_name, date.day_name)
        num_same = self.__fuzzy_eq(self.day_number, date.day_number)

        if name_same and num_same:
            return True

        else:
            return False

    def __fuzzy_eq(self, v1, v2):
        if v1 == v2 or v1 is None or v2 is None:
            return True

        return False


    def __eq__(self, date):
        name_same = (self.day_name == date.day_name)
        num_same = (self.day_number == date.day_number)

        if name_same and num_same:
            return True

        else:
            return False

    def __repr__(self):
        return f"{self.day_number} {self.day_name}"
