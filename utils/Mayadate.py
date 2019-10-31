from CalendarRound import CalendarRound
from LongCount import LongCount

class Mayadate:
    def __init__(self, long_count=LongCount(), calendar_round=CalendarRound()):
        self.long_count = long_count
        self.calendar_round = calendar_round

    def __add__(self, dist):
        return Mayadate(self.long_count + dist.long_count,
            self.calendar_round + dist.calendar_round)

    def __sub__(self, date):
        return Mayadate(self.long_count - dist.long_count,
            self.calendar_round - dist.calendar_round)








if __name__ == "__main__":
    print("hi")
