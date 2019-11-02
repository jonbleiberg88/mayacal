from LongCount import LongCount

class DistanceNumber(LongCount):
    def __init__(self, baktun=0, katun=0, tun=0, winal=0, kin=0, sign=1):
        super().__init__(baktun, katun, tun, winal, kin)
        self.sign = sign

    
