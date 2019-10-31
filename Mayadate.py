class Mayadatedelta(Mayadate):
    self.__init__(self, date, sign):




class Mayadate:
    def __init__(self, long_count=LongCount(), calendar_round=CalendarRound()):
        self.long_count = long_count
        self.calendar_round = calendar_round

    def __add__(self, distance):

        return

    def __sub__(self, date):
        return2



class LongCount:
    def __init__(self, baktun=0, katun=0, tun=0, winal=0, kin=0):
        self.baktun = baktun
        self.katun = katun
        self.tun = tun
        self.winal = winal
        self.kin = kin

    def __add__(self, dist=LongCount()):
        
        kin, carry = self.__add_and_carry(self.kin, dist.kin, 0, 20)
        winal, carry = self.__add_and_carry(self.winal, dist.winal, carry, 18)
        tun, carry = self.__add_and_carry(self.tun, dist.tun, carry, 20)
        katun, carry = self.__add_and_carry(self.katun, dist.katun, carry, 20)
        baktun, carry = self.__add_and_carry(self.baktun, dist.baktun, carry, 20)

        return LongCount(baktun, katun, tun, winal, kin)

    def __add_and_carry(val_1, val_2, carry, max):
        raw_sum = val_1 + val_2

        return raw_sum % max, int(raw_sum >= max)

    def get_calendar_round(self):
        return

class CalendarRound:
    def __init__(self, haab=Haab(), tzolkin=Tzolkin()):
        self.haab = haab
        self.haab_num = haab_num

        self.tzolkin = tzolkin
        self.tzolkin_num = tzolkin_num

    def get_long_count(self):
        return []

class Tzolkin:
    def __init__(self, day_name="Ajaw", day_number=8):
        self.day_name = day_name
        self.day_number = day_number

class Haab:
    def __init__(self, month_name="Kumku", month_number=4):
        self.month_name = month_name
        self.month_number = month_number
