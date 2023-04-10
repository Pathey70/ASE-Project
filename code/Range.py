from Sym import Sym
from Num import Num

class Range:
    def __init__(self, at, txt, lo, hi=None):
        self.at = at
        self.txt = txt
        self.lo = lo
        self.hi = lo or hi or lo
        self.y = Sym()
