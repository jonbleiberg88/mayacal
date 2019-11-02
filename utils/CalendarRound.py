from Haab import Haab
from Tzolkin import Tzolkin

class CalendarRound:
    def __init__(self, haab=Haab(), tzolkin=Tzolkin()):
        self.haab = haab
        self.tzolkin = tzolkin

        self.__check_valid()


    def add_days(self, num_days):
        self.haab.add_days(num_days)
        self.tzolkin.add_days(num_days)


    def __check_valid(self):
        if self.haab.month_number % 5 == 0:
            if self.tzolkin.day_name not in ("Kaban", "Ik", "Manik", "Eb"):
                raise ValueError("Invalid Haab month coefficient, Tzolkin day name combo")

        elif self.haab.month_number % 5 == 1:
            if self.tzolkin.day_name not in ("Etznab", "Akbal", "Lamat", "Ben"):
                raise ValueError("Invalid Haab month coefficient, Tzolkin day name combo")

        elif self.haab.month_number % 5 == 2:
            if self.tzolkin.day_name not in ("Kawak", "Kan", "Muluk", "Ix"):
                raise ValueError("Invalid Haab month coefficient, Tzolkin day name combo")

        elif self.haab.month_number % 5 == 3:
            if self.tzolkin.day_name not in ("Ajaw", "Chikchan", "Ok", "Men"):
                raise ValueError("Invalid Haab month coefficient, Tzolkin day name combo")

        elif self.haab.month_number % 5 == 4:
            if self.tzolkin.day_name not in ("Imix", "Kimi", "Chuwen", "Kib"):
                raise ValueError("Invalid Haab month coefficient, Tzolkin day name combo")

        else:
            raise ValueError(f"Invalid month coefficient {self.haab.month_number}")


    def get_long_count(self):
        return []
