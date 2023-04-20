class RX:
    def __init__(self, t, s):
        t.sort()
        self.name = s if s else ""
        self.rank = 0
        self.n = len(t)
        self.show = ""
        self.has = t