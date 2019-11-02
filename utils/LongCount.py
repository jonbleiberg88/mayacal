class LongCount:
    def __init__(self, baktun=0, katun=0, tun=0, winal=0, kin=0):
        if baktun >= 20:
            raise ValueError("Baktun must be between 0 and 19")
        self.baktun = baktun
        if katun >= 20:
            raise ValueError("Katun must be between 0 and 19")
        self.katun = katun

        if tun >= 20:
            raise ValueError("Tun must be between 0 and 19")
        self.tun = tun

        if winal >= 18:
            raise ValueError("Winal must be between 0 and 17")
        self.winal = winal

        if kin >= 20:
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

    def get_total_kin(self):
        return (self.kin + (self.winal * 20) + (self.tun * 20 * 18) +
            (self.katun * 18 * (20 ** 2)) + (self.baktun * 18 * (20 ** 3)))

    def get_calendar_round(self):
        return

    def __repr__(self):
        return f"{self.baktun}.{self.katun}.{self.tun}.{self.winal}.{self.kin}"
