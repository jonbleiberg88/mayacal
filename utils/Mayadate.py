from CalendarRound import *
from LongCount import *

class Mayadate:
    def __init__(self, long_count=None, calendar_round=None):
        if long_count is None:
            self.LongCount = LongCount(None, None, None, None, None)
        else:
            self.long_count = long_count

        if calendar_round is None:
            if not self.long_count.has_missing():
                self.calendar_round = self.long_count.get_calendar_round()
            else:
                self.calendar_round = CalendarRound(None, None)
        else:
            self.calendar_round = calendar_round

    def has_missing(self):
        return (self.long_count.has_missing() or self.calendar_round.has_missing())

    def add_days(self, num_days, in_place=False):
        if in_place:
            self.long_count = self.long_count.add_days(num_days)
            self.calendar_round = self.calendar_round.add_days(num_days)

            return self
        else:
            return Mayadate(self.long_count.add_days(num_days),
                self.calendar_round.add_days(num_days))

    def infer_long_count_dates(self):
        return self.__infer_lc_recursive(self.long_count.to_list(), [])

    def __infer_lc_recursive(self, lc, poss_dates):
        if None not in lc:
            print(lc)
            if self.calendar_round.match(LongCount(*lc).get_calendar_round()):
                return LongCount(*lc)
            return

        max_vals = [13,20,20,18,20]

        for idx, v in enumerate(zip(lc, max_vals)):
            val, max = v
            if val is None:
                for i in range(max):
                    lc_test = lc[:]
                    lc_test[idx] = i
                    res = self.__infer_lc_recursive(lc_test, poss_dates)
                    if type(res) is LongCount:
                        poss_dates.append(res)

        return poss_dates

    def to_julian_day(self, correlation=584283):
        return self.long_count.to_julian_day(correlation)

    def to_julian(self, correlation=584283):
        return self.long_count.to_julian(correlation)

    def to_gregorian(self, correlation=584283):
        return self.long_count.to_gregorian(correlation)


    def __add__(self, dist):
        lc = self.long_count + dist.long_count

        return lc.get_mayadate()

    def __sub__(self, dist):
        lc = self.long_count - dist.long_count

        return lc.get_mayadate()


    def __repr__(self):
        return f"{self.long_count.__repr__()}  {self.calendar_round.__repr__()}"

class Mayadatedelta(Mayadate):
    def __init__(self, date=None, sign=1):
        self.date = date
        self.sign = sign

    def __repr__(self):
        if self.sign == 1:
            return self.date.__repr__()
        else:
            return f"-{self.date.__repr__()}"






if __name__ == "__main__":
    print("hi")
