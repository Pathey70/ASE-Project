import math
from collections import defaultdict


class Sym:
    """Summarize stream of symbols"""
    def __init__(self, at=0, txt=""):
        self.at = at
        self.txt = txt
        self.n = 0
        self.has = defaultdict(int)
        self.most = 0
        self.mode = None

    def add(self, x,n=1):
        if x != '?':
            self.n += n
            self.has[x] += n
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        """Returns mode"""
        return self.mode

    def div(self):
        """Returns entropy"""
        def fun(p):
            return p * math.log(p, 2)

        e = 0
        for n in self.has.values():
            e += fun(n / self.n)

        return -e

    def rnd(self, x, n):
        return x

    def dist(self, s1, s2):
        if s1 == '?' and s2 == '?':
            return 1
        elif s1 == s2:
            return 0
        else:
            return 1
