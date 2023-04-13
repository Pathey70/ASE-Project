import sys

import TestEngine
from Sym import Sym
from Num import Num
from Data import Data
from Utils import *
from Discretization import bins
from collections import defaultdict

tot = 0


def count(t):
    global tot
    tot = tot + len(t)


def eg_syms(the):
    """Tests Sym"""
    sym = Sym()
    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x)
    print(sym.mid(), rnd(sym.div()))
    assert 1.38 == rnd(sym.div())


# def eg_nums(the):
#     """Tests Num"""
#     num1 = Num(the)
#     num2 = Num(the)
#     Seed = the['seed']
#     for i in range(1, 1001):
#         x, Seed = rand(0, 1, Seed)
#         num1.add(x)
#     Seed = the['seed']
#     for i in range(1, 1001):
#         x, Seed = rand(0, 1, Seed)
#         num2.add(x ** 2)
#     m1 = rnd(num1.mid(), 1)
#     m2 = rnd(num2.mid(), 1)
#     d1 = rnd(num1.div(), 1)
#     d2 = rnd(num2.div(), 1)
#     print(1, m1, d1)
#     print(2, m2, d2)
#     assert num1.mid() > num2.mid() and .5 == m1
#
#
# def eg_is(the):
#     print(the)
#     pass
#
#
# def eg_rand(the):
#     t = []
#     u = []
#     Seed = the['seed']
#     for i in range(1, 1001):
#         t.append(rint(0, 100))
#     Seed = the['seed']
#     for i in range(1, 1001):
#         u.append(rint(0, 100))
#     for i in range(1, 1000):
#         assert t[i] == u[i]
#
#
# def eg_some(the):
#     the['Max'] = 32
#     num1 = Num(the)
#     for i in range(1, 10001):
#         num1.add(i)
#     print(num1.has)
#
#
# def eg_csv(the):
#     csv(the['file'], count)
#     assert tot == 3192
#
#
# def eg_data(the):
#     """Tests Data"""
#     data = Data(the['file'], the)
#     col = data.cols.x[1]
#     print(col.lo, col.hi, col.mid(), col.div())
#     print(data.stats(1, data.cols.y, 'mid'))
#
#
# def eg_half(the):
#     data = Data(the["file"], the)
#     left, right, A, B, mid, c, _ = data.half()
#     print(len(left), len(right))
#     l, r = data.clone(left), data.clone(right)
#     # print(A.cells, c)
#     # print(mid.cells)
#     # print(B.cells)
#     print("l", l.stats(2, l.cols.y))
#     print("r", l.stats(2, r.cols.y))
#
#
# def eg_tree(the):
#     data = Data(the["file"], the)
#     show(data.tree(), "mid", data.cols.y, 1)


def eg_sway(the):
    data = Data(the["file"], the)
    best, rest, _ = data.sway()
    print("\nall ", data.stats(2, data.cols.y))
    print("    ", data.stats(2, data.cols.y, 'div'))
    print("\nbest", data.stats(2, best.cols.y))
    print("    ", data.stats(2, best.cols.y, 'div'))
    print("\nrest", data.stats(2, rest.cols.y))
    print("    ", data.stats(2, rest.cols.y, 'div'))
    print("\nall ~= best?", diffs(best.cols.y, data.cols.y, the))
    print("best ~= rest?", diffs(best.cols.y, rest.cols.y, the))


#
# def eg_clone(the):
#     data1 = Data(the['file'], the)
#     data2 = data1.clone(data1.rows)
#     print(data1.stats(1, data1.cols.y))
#     print(data2.stats(1, data2.cols.y))
#
#
# def eg_cliffs(the):
#     assert False == cliffs_delta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3], the)
#     assert True == cliffs_delta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6], the)
#     t1 = []
#     t2 = []
#     Seed = the['seed']
#     for i in range(1, 1001):
#         x, Seed = rand(0, 1, Seed)
#         t1.append(x)
#     Seed = the['seed']
#     for i in range(1, 1001):
#         x, Seed = rand(0, 1, Seed)
#         t2.append(x ** (0.5))
#     assert False == cliffs_delta(t1, t1, the, Seed)
#     assert True == cliffs_delta(t1, t2, the, Seed)
#
#     diff = False
#     j = 1.0
#
#     def func(x):
#         return x * j
#
#     while not diff:
#         t3 = list(map(func, t1))
#         diff = cliffs_delta(t1, t3, the)
#         print('>', rnd(j), diff)
#         j = j * 1.025
#
#
# def eg_dist(the):
#     data = Data(the['file'], the)
#     num = Num(the)
#     for row in data.rows:
#         num.add(data.dist(row, data.rows[0]))
#     d = {'lo': num.lo, 'hi': num.hi, 'mid': rnd(num.mid()), 'div': rnd(num.div())}
#     print(d)
#
#
# def eg_bins(the):
#     b4=""
#     data = Data(the['file'], the)
#     best, rest, _ = data.sway()
#     print("all\t\t\tbest:{}, rest:{}".format(len(best.rows), len(rest.rows)))
#     for k, t in enumerate(bins(data.cols.x, {"best": best.rows, "rest": rest.rows}, the)):
#         for rng in t:
#             if rng.txt != b4:
#                 print("")
#             b4=rng.txt
#             print(rng.txt, rng.lo, rng.hi, rnd(value(rng.y.has, len(best.rows), len(rest.rows), "best")), dict(rng.y.has))
#
# def eg_xpln(the):
#     data = Data(the['file'], the)
#     best, rest, evals = data.sway()
#     rule,most= data.xpln(best,rest)
#     print("\n-----------\nexplain=", showRule(rule))
#     data1= data.clone([i for i in selects(rule,data.rows) if i!=None])
#     print("all               ",data.stats(2, best.cols.y),data.stats(2, best.cols.y,'div'))
#     print("sway with ",evals,"evals",best.stats(2, best.cols.y),best.stats(2, best.cols.y,"div"))
#     print("xpln with ",evals,"evals",data1.stats(2, data1.cols.y),data1.stats(2, data1.cols.y,"div"))
#     top,_ = data.betters(len(best.rows))
#     top = data.clone(top)
#     print("sort with ",len(data.rows),"evals",top.stats(2, top.cols.y),top.stats(2, top.cols.y,"div"))

def eg_sway1(the):
    ans = defaultdict(int)
    ans2 = defaultdict(int)
    for i in range(0, 20):
        print('*********')
        the['seed'] = 937162211 - i * 100
        data = Data(the["file"], the)
        data1 = Data(the["file"], the)
        data2 = Data(the["file"], the)
        best, rest, _ = data.sway()
        best1, rest1 = data.sway_kmeans()
        best2, rest2 = data.sway_agglo()
        best3, rest3 = data.sway_pca()
        best4, rest4 = data.sway_spectral()
        print("\nall ", data.stats(2, data.cols.y))
        x = data.stats(2, best.cols.y)
        print("sway1", x)
        x1 = data1.stats(2, best1.cols.y)
        print("sway2", x1)
        x2 = data2.stats(2, best2.cols.y)
        print("sway3", x2)
        x3 = data2.stats(2, best3.cols.y)
        print("sway4", x3)
        x4 = data2.stats(2, best4.cols.y)
        print("sway5", x4)
        print("all ~= sway1?", diffs(best.cols.y, data.cols.y, the))
        print("sway2 ~= sway1?", diffs(best.cols.y, best1.cols.y, the))
        # print("sway3 ~= sway1?", diffs(best.cols.y, best2.cols.y, the))
        print("all ~= all?", diffs(data.cols.y, data.cols.y, the))
    #     try:
    #         rule,most= data.xpln(best,rest)
    #     except:
    #         continue
    #
    #     data1= data.clone([i for i in selects(rule,data.rows) if i!=None])
    #     x = data1.stats(2, data1.cols.y)
    #     print("xpln1", x)
    #     for k in x:
    #         ans[k] = ans[k] + x[k]
    #
    #     top2, _ = data.betters(len(best.rows))
    #     data2 = data.clone(top2)
    #     x2 = data2.stats(2, data2.cols.y)
    #     print("top", x2)
    #     for k in x2:
    #         ans2[k] = ans2[k] + x2[k]
    #     try:
    #         print("xpln ~= sway1?", diffs(best.cols.y, data1.cols.y, the))
    #         print("top ~= sway1?", diffs(data2.cols.y, best.cols.y, the))
    #     except:
    #         pass
    #
    # for k in ans:
    #     ans[k] = round(ans[k]/20,2)
    # for k in ans2:
    #     ans2[k] = round(ans2[k]/20,2)
    # print("xpln1",dict(ans))
    # print("top",dict(ans2))
