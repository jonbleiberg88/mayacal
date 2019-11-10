
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
    def __init__(self, day_number=None, day_name=None, tzolkin_num=None):
        if tzolkin_num is not None:
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
        if new_num >= 260:
            raise ValueError("Invalid Tzolkin number, must be between 0 and 259")

        self.tzolkin_num = new_num
        self.day_number, self.day_name = tzolkin_num_to_day[self.tzolkin_num]

    def add_days(self, num_days):
        new_num = (self.tzolkin_num + num_days) % 260
        self.reset_by_tzolkin_num(new_num)

        return self

    def __eq__(self, date):
        if self.day_name == date.day_name and self.day_number == date.day_number:
            return True
        else:
            return False

    def __repr__(self):
        return f"{self.day_number} {self.day_name}"
