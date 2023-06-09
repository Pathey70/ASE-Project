import math
from Main import coerce
import os
import random
import numpy as np
from Sym import Sym
from itertools import combinations
import pandas as pd


def rnd(n, nPlaces=2):
    mult = pow(10, nPlaces)
    return math.floor(n * mult + 0.5) / mult


def rand(lo=0, hi=1, Seed=937162211):
    # Seed=937162211
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi - lo) * Seed / 2147483647, Seed


def rint(lo, hi):
    x, seed = rand(lo, hi)
    return math.floor(0.5 + x)


def row_cleaning(rows):
    cleaned_rows = []
    for row in rows:
        flag = True
        for cell in row.cells:
            if isinstance(cell, str) and cell.strip() == '?':
                flag = False
                break
        if flag:
            cleaned_rows.append(row)
    return cleaned_rows


def csv(src, fun):
    if not os.path.isfile(src):
        print("\nfile " + src + " doesn't exists!")
        sys.exit(2)
    with open(src, 'r') as file1:
        for line in file1:
            temp = []
            for j in line.strip().split(','):
                temp.append(coerce(j))
            fun(temp)


def csv_stats(filename):
    data = pd.read_csv(filename)
    print(data.describe())

def mp(src, fun):
    for i in src:
        # print(i)
        fun(i)


def kap(t, fun, u={}):
    u = {}
    for k, v in enumerate(t):
        v, k = fun(k, v)
        if not k:
            u[len(u)] = v
        else:
            u[k] = v
    return u


def kap1(t, fun, u={}):
    u = {}
    for k, v in t.items():
        v, k = fun(k, v)
        if not k:
            u[len(u)] = v
        else:
            u[k] = v
    return u


def cosine(a, b, c):
    if c == 0:
        c = 0.5
    x1 = (a ** 2 + c ** 2 - b ** 2) / (2 * c)
    x2 = max(0, min(1, x1))
    y = math.sqrt(abs(a ** 2 - x2 ** 2))
    return x2, y


def many(t, n, seed=937162211):
    random.seed(seed)
    return random.choices(t, k=n)


def any(t, seed=937162211):
    random.seed(seed)
    return random.choices(t)[0]


def per(t, p=0.5):
    p = math.floor((p * len(t)) + .5)
    return t[max(1, min(len(t), p))]


def show(node, what, cols, nPlaces, lvl=0):
    if node:
        print("| " * lvl + str(len(node["data"].rows)) + " ", end='')
        # print(node)
        if "left" not in node or lvl == 0:
            print(node["data"].stats(nPlaces, node["data"].cols.y, "mid"))
        else:
            print("")
        show(None if "left" not in node else node["left"], what, cols, nPlaces, lvl + 1)
        show(None if "right" not in node else node["right"], what, cols, nPlaces, lvl + 1)


def cliffs_delta(ns1, ns2, the, seed=937162211):
    if len(ns1) > 256:
        ns1 = many(ns1, 256, seed)
    if len(ns2) > 256:
        ns2 = many(ns2, 256, seed)
    if len(ns1) > 10 * len(ns2):
        ns2 = many(ns1, 10 * len(ns2), seed)
    if len(ns2) > 10 * len(ns1):
        ns2 = many(ns2, 10 * len(ns1), seed)

    n, gt, lt = 0, 0, 0
    for x in ns1:
        for y in ns2:
            n = n + 1
            if x > y:
                gt = gt + 1

            elif x < y:
                lt = lt + 1
    return abs(lt - gt) / n > the['cliffs']


def diffs(nums1, nums2, the):
    def func(k, nums):
        return cliffs_delta(nums.has, nums2[k].has, the), nums.txt

    return kap(nums1, func)


def extend(rng, n, s, the):
    rng.lo = min(rng.lo, n)
    rng.hi = max(rng.hi, n)
    rng.y.add(s)


def value(has, nB=1, nR=1, sGoal=True):
    b = r = 0
    for x, n in has.items():
        if x == sGoal:
            b += n
        else:
            r += n
    b, r = b / (nB + 1 / math.inf), r / (nR + 1 / math.inf)
    return b ** 2 / (b + r)


def showRule(rule, merge=None, merges=None, pretty=None):
    def pretty(rangeR):
        return rangeR['lo'] if rangeR['lo'] == rangeR['hi'] else [rangeR['lo'], rangeR['hi']]

    def merge(t0):
        right = {}
        left = {}
        j = 1
        t = []
        while j <= len(t0):
            left = t0[j - 1]
            right = None if j == len(t0) else t0[j]
            if right and left['hi'] == right['lo']:
                left['hi'] = right['hi']
                j = j + 1
            t.append({'lo': left['lo'], 'hi': left['hi']})
            j = j + 1
        return t if len(t0) == len(t) else merge(t)

    def merges(attr, ranges):
        temp = merge(sorted(ranges, key=lambda x: x['lo']))
        # print(temp)
        return list(map(pretty, temp)), attr

    return kap1(rule, merges)


def firstN(sortedRanges, scoreFun):
    def print_range(r):
        print(r['range'].txt, r['range'].lo, r['range'].hi, rnd(r['val']),
              dict(r['range'].y.has))  # rnd(r.val) missing, Range has no val, maybe requires some change

    # print()
    # mp(sortedRanges, print_range)
    first = sortedRanges[0]['val']

    # print()

    def useful(rng):
        if rng['val'] > 0.05 and rng['val'] > first / 2:
            return rng

    sortedRanges = list(map(useful, sortedRanges))
    most, out = -1, -1
    sortedRanges = [i for i in sortedRanges if i != None]
    arr = [i['range'] for i in sortedRanges]
    for n in range(1, len(sortedRanges) + 1):
        comb = list(combinations(arr, n))
        for c in comb:
            tmp, rule = scoreFun(c)
            if tmp and tmp > most:
                out, most = rule, tmp

    # print("out1 and most1", out, most)
    # most, out = -1, -1
    # for n in range(1, len(sortedRanges) + 1):
    #     tmp, rule = scoreFun([i['range'] for i in sortedRanges[:n]])
    #     if tmp and tmp > most:
    #         out, most = rule, tmp
    # print("out2 and most2", out, most)
    return out, most


def selects(rule, rows):
    def disjunction(ranges, row):
        if ranges:
            for rng in ranges:
                lo, hi, at = rng['lo'], rng['hi'], rng['at']
                x = row.cells[at]  # Might need a change to row.cells[at]
                if x == '?' or (lo == hi and lo == x) or (lo <= x and x < hi):
                    return True
        return False

    def conjunction(row):
        for _, ranges in rule.items():
            if not disjunction(ranges, row):
                return False
        return True

    def get_row(r):
        if conjunction(r):
            return r

    return list(map(get_row, rows))
