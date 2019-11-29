from Haab import *
from Tzolkin import *

class CalendarRound:
    def __init__(self, tzolkin=None, haab=None):
        if tzolkin is None:
            self.tzolkin = Tzolkin(None, None)
        else:
            self.tzolkin = tzolkin

        if haab is None:
            self.haab = Haab(None, None)
        else:
            self.haab = haab

        self.__check_valid()

    def has_missing(self):
        return (self.tzolkin.has_missing() or self.haab.has_missing())


    def add_days(self, num_days, in_place=False):
        if in_place:
            self.haab.add_days(num_days, True)
            self.tzolkin.add_days(num_days, True)

            return self

        else:
            new_haab = self.haab.add_days(num_days)
            new_tzolkin = self.tzolkin.add_days(num_days)

            return CalendarRound(new_tzolkin, new_haab)


    def __check_valid(self):
        if self.haab.month_number is None or self.tzolkin.day_name is None:
            return

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


    def get_long_count_possibilities(self, min_date, max_date):
        from LongCount import LongCount, kin_to_long_count
        min_cal_round = min_date.get_calendar_round()
        init_num = tzolkin_day_to_num[(min_cal_round.tzolkin.day_number, min_cal_round.tzolkin.day_name)]
        day_num = tzolkin_day_to_num[(self.tzolkin.day_number, self.tzolkin.day_name)]

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
            lc = lc.add_days(18980) #LCM of 260 and 365


    def match(self, date):
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
