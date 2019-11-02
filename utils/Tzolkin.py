
tzolkin_days = ["Imix", "Ik", "Akbal", "Kan", "Chikchan", "Kimi", "Manik",
                    "Lamat", "Muluk", "Ok", "Chuwen", "Eb", "Ben", "Ix",
                    "Men", "Kib", "Kaban", "Etznab", "Kawak", "Ajaw"]

tzolkin_idx_to_day = {idx:day for idx, day in enumerate(tzolkin_days)}
tzolkin_day_to_idx = {day:idx for idx, day in tzolkin_day_to_idx.keys()}

class Tzolkin:
    def __init__(self, day_name="Ajaw", day_number=4):
        self.day_name = day_name
        self.day_number = day_number

    def add_days(self, days):
        return
