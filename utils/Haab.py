haab_months = ["Pop", "Wo", "Sip", "Sotz", "Sek", "Xul", "Yaxkin", "Mol", "Chen",
                "Yax", "Sak", "Keh", "Mak", "Kankin", "Muwan", "Pax", "Kayab",
                "Kumku", "Wayeb"]

haab_idx_to_month = {idx:month for idx, month in enumerate(haab_months)}
haab_month_to_idx = {month:idx for idx, month in haab_idx_to_month.items()}


class Haab:
    def __init__(self, month_number=None, month_name=None):
        if month_name not in haab_months and month_name is not None:
            raise ValueError(f"Invalid Haab month name {month_name}")
        self.month_name = month_name

        if month_name == "Wayeb":
             if month_number not in list(range(5)):
                 raise ValueError("Invalid Haab month number, Wayeb number must be between 0 and 4")
        elif month_number not in list(range(20)) and month_number is not None:
            raise ValueError("Invalid Haab month number, must be an integer between 0 and 19 or NoneType")

        self.month_number = month_number

        if not self.has_missing():
            self.haab_num = 20 * haab_month_to_idx[month_name] + month_number
        else:
            self.haab_num = None

    def has_missing(self):
        if self.month_name is None or self.month_number is None:
            return True

        return False

    def reset_by_haab_num(self, new_num):
        self.month_name = haab_idx_to_month[new_num // 20]
        self.month_number = new_num % 20

        return self

    def add_days(self, num_days, in_place=False):
        new_num = (self.haab_num + num_days) % 365
        if in_place:
            self.haab_num = new_num
            self.reset_by_haab_num(self.haab_num)

            return self
        else:
            return Haab().reset_by_haab_num(new_num)

    def __fuzzy_eq(self, v1, v2):
        if v1 == v2 or v1 is None or v2 is None:
            return True

        return False

    def match(self, date):
        name_same = self.__fuzzy_eq(self.month_name, date.month_name)
        num_same = self.__fuzzy_eq(self.month_number, date.month_number)

        if name_same and month_same:
            return True
        else:
            return False

    def __eq__(self, date):
        name_same = self.month_name == date.month_name
        num_same = self.month_number == date.month_number

        if name_same and month_same:
            return True
        else:
            return False

    def __sub__(self, date):
        return abs(self.haab_num - date.haab_num)


    def __repr__(self):
        return f"{self.month_number} {self.month_name}"
