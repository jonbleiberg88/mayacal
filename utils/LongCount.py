from CalendarRound import *

class LongCount:
    def __init__(self, baktun=0, katun=0, tun=0, winal=0, kin=0):
        if baktun is not None and baktun >= 20:
            raise ValueError("Baktun must be between 0 and 19 or NoneType")
        self.baktun = baktun
        if katun is not None and katun >= 20:
            raise ValueError("Katun must be between 0 and 19 or NoneType")
        self.katun = katun

        if tun is not None and tun >= 20:
            raise ValueError("Tun must be between 0 and 19")
        self.tun = tun

        if winal is not None and winal >= 18:
            raise ValueError("Winal must be between 0 and 17")
        self.winal = winal

        if kin is not None and kin >= 20:
            raise ValueError("Kin must be between 0 and 19")
        self.kin = kin

    def __add__(self, dist):

        kin, carry = self.__add_and_carry(self.kin, dist.kin, 0, 20)
        winal, carry = self.__add_and_carry(self.winal, dist.winal, carry, 18)
        tun, carry = self.__add_and_carry(self.tun, dist.tun, carry, 20)
        katun, carry = self.__add_and_carry(self.katun, dist.katun, carry, 20)
        baktun, carry = self.__add_and_carry(self.baktun, dist.baktun, carry, 20)

        return LongCount(baktun, katun, tun, winal, kin)

    def __add_and_carry(self, val_1, val_2, carry, max):
        raw_sum = val_1 + val_2 + carry

        return raw_sum % max, int(raw_sum >= max)


    def __sub__(self, dist):
        kin_diff = self.get_total_kin() - dist.get_total_kin()
        if kin_diff >= 0:
            return DistanceNumber(kin_to_long_count(kin_diff), sign=1)
        else:
            return DistanceNumber(kin_to_long_count(kin_diff * -1), sign=-1)


    def get_total_kin(self):
        return (self.kin + (self.winal * 20) + (self.tun * 20 * 18) +
            (self.katun * 18 * (20 ** 2)) + (self.baktun * 18 * (20 ** 3)))

    def get_calendar_round(self):
        # Mythological start date
        initial_date = CalendarRound(Tzolkin(4, "Ajaw"), Haab(8, "Kumku"))
        initial_date.add_days(self.get_total_kin())

        return initial_date

    def get_mayadate(self):
        from Mayadate import Mayadate
        return Mayadate(self, self.get_calendar_round())

    def add_days(self, num_days):
        self = kin_to_long_count(self.get_total_kin() + num_days)
        return self

    def get_glyph_g(self):
        g_num = (self.winal * 20 + self.kin)  % 9
        if g_num == 0:
            g_num = 9
        return f"G{g_num}"

    def to_list(self):
        return [self.baktun, self.katun, self.tun, self.winal, self.kin]

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
        return f"{self.baktun}.{self.katun}.{self.tun}.{self.winal}.{self.kin}"

class DistanceNumber(LongCount):
    def __init__(self, long_count=LongCount(), sign=1):
        self.long_count = long_count
        super().__init__(long_count.baktun, long_count.katun, long_count.tun,
            long_count.winal, long_count.kin)
        self.sign = sign

    def get_total_kin(self):
        return  self.sign * super().get_total_kin()


    def __repr__(self):
        if self.sign == 1:
            return self.long_count.__repr__()

        else:
            return f"-{self.long_count.__repr__()}"

def kin_to_long_count(num_kin):
    long_count = LongCount()

    long_count.baktun = num_kin // (18 * (20 ** 3))
    num_kin = num_kin - (long_count.baktun * 18 * (20 ** 3))

    long_count.katun = num_kin // (18 * (20 ** 2))
    num_kin = num_kin - (long_count.katun * 18 * (20 ** 2))

    long_count.tun = num_kin // (18 * 20)
    num_kin = num_kin - (long_count.tun * 18 * 20)

    long_count.winal = num_kin // 20
    num_kin = num_kin - (long_count.winal * 20)

    long_count.kin = num_kin

    return long_count
