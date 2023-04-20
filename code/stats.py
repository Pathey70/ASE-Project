import math
import random
from Num import Num
from RX import RX
from Utils import samples, merge, cliffsDelta, mid, div


def erf(x):
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y


def gaussian(mu=0, sd=1):
    return mu + sd * math.sqrt(-2 * math.log(random.random())) * math.cos(2 * math.pi * random.random())


def delta(i, other):
    e, y, z = 1e-32, i, other
    return abs(y.mu - z.mu) / ((e + y.sd ** 2 / y.n + z.sd ** 2 / z.n) ** 0.5)


def bootstrap(y0, z0, the):
    x, y, z, yhat, zhat = Num(), Num(), Num(), [], []
    for y1 in y0:
        x.add(y1)
        y.add(y1)
    for z1 in z0:
        x.add(z1)
        z.add(z1)
    xmu, ymu, zmu = x.mu, y.mu, z.mu
    for y1 in y0:
        yhat.append(y1 - ymu + xmu)
    for z1 in z0:
        zhat.append(z1 - zmu + xmu)

    tobs = delta(y, z)
    n = 0
    for _ in range(the['bootstrap']):
        if delta(Num(samples(yhat)), Num(samples(zhat))) > tobs:
            n += 1
    return n / the['bootstrap'] >= the['conf']


def scottKnot(rxs, the):
    def merges(i, j):
        out = RX([], rxs[i].name)
        for k in range(i, j+1):
            out=merge(out, rxs[j])
        return out

    def same(lo, cut, hi):
        left = merges(lo, cut)
        right = merges(cut + 1, hi)
        return cliffsDelta(left.has, right.has, the) and bootstrap(left.has, right.has, the)

    def recurse(lo, hi, rank):
        cut = None
        b4 = merges(lo, hi)
        best = 0
        for j in range(lo, hi+1):
            if j < hi:
                l = merges(lo, j)
                r = merges(j + 1, hi)
                now = (l.n * (mid(l) - mid(b4)) ** 2 + r.n * (mid(r) - mid(b4)) ** 2) / (l.n + r.n)
                if now > best:
                    if abs(mid(l) - mid(r)) >= cohen:
                        cut, best = j, now
        if cut and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank = recurse(cut + 1, hi, rank)
        else:
            for i in range(lo, hi):
                rxs[i].rank = rank
        return rank

    rxs.sort(key=lambda x: mid(x))
    cohen = div(merges(1, len(rxs)-1)) * the['cohen']
    recurse(1, len(rxs)-1, 1)
    return rxs


def tiles(rxs, the):
    huge = math.inf
    lo, hi = huge, -math.inf
    for rx in rxs:
        lo, hi = min(lo, rx.has[0]), max(hi, rx.has[len(rx.has) - 1])
    for rx in rxs:
        t, u = rx.has, []

        def of(x, most):
            return int(max(1, min(x, most)))

        def at(x):
            return t[of(len(t) * x//1, len(t))]

        def pos(x):
            return math.floor(of(the['width'] * (x - lo) / (hi - lo + 1E-32) // 1, the['width']))

        for i in range(0, the['width'] + 1):
            u.append(" ")
        a, b, c, d, e = at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E = pos(a), pos(b), pos(c), pos(d), pos(e)

        for i in range(A, B + 1):
            u[i] = "-"
        for i in range(D, E + 1):
            u[i] = "-"

        u[the['width']//2] = "|"
        u[C] = "*"

        rx.show = rx.show + ''.join(u) + "{" + the["Fmt"].format(a)
        for x in [b, c, d, e]:
            rx.show = rx.show + ", " + the["Fmt"].format(x)
        rx.show = rx.show + "}"
    return rxs
