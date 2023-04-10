import math
from Utils import rnd, rand, rint, per


class Num:
    """Summarize stream of numbers"""
    def __init__(self, the={}, at=0, txt=""):
        self.at = at
        self.txt = txt
        self.n = self.mu = self.m2 = 0
        self.lo = math.inf
        self.hi = -math.inf
        self.has = {}
        self.ok = True
        self.the = the
        self.w = -1 if '-' in self.txt else 1

    def add(self, x, n=1):
        if x != '?':
            # self.n += 1
            
            
            self.n += 1
            self.lo = min(x, self.lo)
            self.hi = max(x, self.hi)
            d = x - self.mu
            self.mu += d/self.n     # Might have to replace with integer division
            self.m2 += d * (x - self.mu)
            all = len(self.has)
            t, _ = rand()
            if self.the['Max'] > all:
                pos = all+1
            elif t < self.the['Max']/self.n:
                pos = rint(1,all)
            else:
                pos = 0
            if pos:
                self.has[pos] = x
                self.ok = False

    def has_f(self):
        temp = sorted(self.has.items(),key=lambda x:x[1])
        temp = dict(temp)
        self.ok = True
        return list(temp.values())

    def mid(self):
        """Returns mean"""
        return self.mu

    def div(self):
        """Return standard deviation"""
        return 0 if self.m2 < 0 or self.n < 2 else pow(self.m2/(self.n - 1), 0.5)

    def rnd(self, x, n):
        return x if x == '?' else rnd(x, n)

    def norm(self, n):
        if n == '?':
            return n
        return (n - self.lo) / (self.hi - self.lo + 1e-32)

    def dist(self, n1, n2):
        if n1 == '?' and n2 == '?':
            return 1
        n1, n2 = self.norm(n1), self.norm(n2)
        if n1 == "?":
            n1 = 1 if n2 < 0.5 else 0
        if n2 == "?":
            n2 = 1 if n1 < 0.5 else 0
        return abs(n1 - n2)
