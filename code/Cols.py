import re
from Sym import Sym
from Num import Num


class Cols:
    """Factory for creating NUMs and SYMs"""
    def __init__(self, the,t):
        self.names = t
        self.all = []
        self.klass = None
        self.x = []
        self.y = []
        for n, s in enumerate(t):
            if re.match('^[A-Z]+', s):
                col = Num(the, n, s)
            else:
                col = Sym(n, s)
            self.all.append(col)
            if s[-1] != 'X':
                if '!' in s:
                    self.klass = col
                if s[-1] in ['+', '-','!']:
                    self.y.append(col)
                else:
                    self.x.append(col)

    def add(self, row):
        for t in [self.x, self.y]:
            for col in t:
                col.add(row.cells[col.at])