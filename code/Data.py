from Utils import *
from Row import Row
from Cols import Cols
from Discretization import bins
import math
import functools
import random
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering
from sklearn.decomposition import PCA


class Data:
    """Container for ROWs, summarized into NUM or SYM columns"""

    def __init__(self, src={}, the=None):
        self.rows = list()
        self.cols = None
        self.the = the
        random.seed(self.the['seed'])
        if type(src) == str:
            csv(src, self.add)
        else:
            mp(src, self.add)

    def add(self, t):
        """Adds rows and columns"""
        if not self.cols:
            self.cols = Cols(self.the, t)
        else:
            if type(t) == list:
                t = Row(t)
            # print(t)
            self.cols.add(t)
            self.rows.append(t)

    def clone(self, t={}):
        """Creates clone"""
        data = Data([self.cols.names], self.the)
        mp(t, data.add)
        return data

    def stats(self, nPlaces, cols=None, what='mid'):
        if not cols:
            cols = self.cols.x

        def fun(k, col):
            return col.rnd(getattr(col, what)(), nPlaces), col.txt

        return kap(cols, fun)

    def dist(self, row1, row2, cols=None):
        n = 0
        d = 0
        if not cols:
            cols = self.cols.x
        for _, col in enumerate(cols):
            n = n + 1
            d = d + col.dist(row1.cells[col.at], row2.cells[col.at]) ** self.the['p']
        return (d / n) ** (1 / self.the['p'])

    def better(self, row1, row2, s1=0, s2=0, ys=None, x=0, y=0):
        if not ys:
            ys = self.cols.y
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(ys))
            s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        return s1 / len(ys) < s2 / len(ys)

    def better_multiple(self, rows1, rows2, s1=0, s2=0, ys=None, x=0, y=0):
        if not ys:
            ys = self.cols.y
        for col in ys:
            for row1, row2 in zip(rows1, rows2):
                x = col.norm(row1.cells[col.at])
                y = col.norm(row2.cells[col.at])
                s1 = s1 - math.exp(col.w * (x - y) / len(ys))
                s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        return s1 / len(ys) < s2 / len(ys)

    def around(self, row1, rows=None, cols=None):
        if not rows:
            rows = self.rows
        if not cols:
            cols = self.cols.x

        def fun(row2):
            return {'row': row2, 'dist': self.dist(row1, row2, cols)}

        return sorted(list(map(fun, rows)), key=lambda x: x['dist'])

    def half_agglo(self, rows=None, cols=None):
        if not rows:
            rows = self.rows

        rows_numpy = np.array([r.cells for r in rows])
        agg = AgglomerativeClustering(n_clusters=2, metric='euclidean', linkage='ward').fit(rows_numpy)
        left = []
        right = []
        for idx, label in enumerate(agg.labels_):
            if label == 0:
                left.append(rows[idx])
            else:
                right.append(rows[idx])
        return left, right, random.choices(left, k=10), random.choices(right, k=10)

    def half_spectral(self, rows=None, cols=None):
        if not rows:
            rows = self.rows

        rows_numpy = np.array([r.cells for r in rows])
        spec = SpectralClustering(n_clusters=2, affinity='nearest_neighbors', n_jobs=10, random_state=self.the['seed']).fit(rows_numpy)
        left = []
        right = []
        for idx, label in enumerate(spec.labels_):
            if label == 0:
                left.append(rows[idx])
            else:
                right.append(rows[idx])
        return left, right, random.choices(left, k=10) if len(left) > 10 else left, random.choices(right, k=10) if len(right) > 10 else right

    def half_variance(self, rows=None, cols=None, above=None):
        if not rows:
            rows = self.rows

        rows_numpy = np.array([r.cells for r in rows])
        pca = PCA(n_components=1)
        rows_transformed = pca.fit_transform(rows_numpy)
        result = [i[1] for i in sorted(enumerate(rows), key=lambda x: rows_transformed[x[0]])]
        left = result[:len(result)//2]
        right = result[len(result)//2:]
        return left, right, random.choices(left, k=10), random.choices(right, k=10)

    def half_kmeans(self, rows=None, cols=None, above=None):
        if not rows:
            rows = self.rows

        rows_numpy = np.array([r.cells for r in rows])
        kmeans = KMeans(n_clusters=2, random_state=self.the['seed'], n_init=10).fit(rows_numpy)
        left = []
        right = []
        lc = Row(kmeans.cluster_centers_[0])
        rc = Row(kmeans.cluster_centers_[1])
        A = None
        B = None

        def calc_min(center, row, A):
            if not A:
                A = row
            if self.dist(A, center) > self.dist(A, row):
                return row
            else:
                return A

        for idx, label in enumerate(kmeans.labels_):
            if label == 0:
                A = calc_min(lc, rows[idx], A)
                left.append(rows[idx])
            else:
                B = calc_min(rc, rows[idx], B)
                right.append(rows[idx])

        return left, right, A, B

    def half(self, rows=None, cols=None, above=None):
        def gap(r1, r2):
            return self.dist(r1, r2, cols)

        if not rows:
            rows = self.rows

        some = many(rows, self.the["Halves"], self.the['seed'])
        if self.the['Reuse']:
            A = above
        if not above or not self.the['Reuse']:
            A = any(some, self.the['seed'])
        B = self.around(A, some)[int(self.the["Far"] * len(rows)) // 1]["row"]

        def dist(row1, row2):
            return self.dist(row1, row2, cols)

        c = dist(A, B)
        left = []
        right = []

        def project(row):
            return {"row": row, "dist": cosine(dist(row, A), dist(row, B), c)}

        for n, tmp in enumerate(sorted(list(map(project, rows)), key=lambda x: x["dist"])):
            if n <= len(rows) // 2:
                left.append(tmp["row"])
                mid = tmp["row"]
            else:
                right.append(tmp["row"])
        if self.the['Reuse'] and above:
            evals = 1
        else:
            evals = 2
        # print(A)
        # print(type(A))
        # print(B)
        # print(type(B))
        return left, right, A, B, mid, c, evals

    def sway_kmeans(self, cols=None):
        def worker(rows, worse):
            if len(rows) <= len(self.rows) ** self.the["min"]:
                return rows, many(worse, self.the['rest'] * len(rows))
            l, r, A, B = self.half_kmeans(rows, cols)
            if self.better(B, A):
                l, r, A, B = r, l, B, A
            for x in r:
                worse.append(x)
            return worker(l, worse)

        rows = row_cleaning(self.rows)
        best, rest = worker(rows, [])
        return self.clone(best), self.clone(rest)

    def sway_agglo(self, cols=None):
        def worker(rows, worse):
            if len(rows) <= len(self.rows) ** self.the["min"]:
                return rows, many(worse, self.the['rest'] * len(rows))
            l, r, A, B = self.half_agglo(rows, cols)
            if self.better_multiple(B, A):
                l, r, A, B = r, l, B, A
            for x in r:
                worse.append(x)
            return worker(l, worse)

        rows = row_cleaning(self.rows)
        best, rest = worker(rows, [])
        return self.clone(best), self.clone(rest)

    def sway_spectral(self, cols=None):
        def worker(rows, worse):
            if len(rows) <= len(self.rows) ** self.the["min"]:
                return rows, many(worse, self.the['rest'] * len(rows))
            l, r, A, B = self.half_spectral(rows, cols)
            if self.better_multiple(B, A):
                l, r, A, B = r, l, B, A
            for x in r:
                worse.append(x)
            return worker(l, worse)

        rows = row_cleaning(self.rows)
        best, rest = worker(rows, [])
        return self.clone(best), self.clone(rest)

    def sway_pca(self, cols=None):
        def worker(rows, worse):
            if len(rows) <= len(self.rows) ** self.the["min"]:
                return rows, many(worse, self.the['rest'] * len(rows))
            l, r, A, B = self.half_variance(rows, cols)
            if self.better_multiple(B, A):
                l, r, A, B = r, l, B, A
            for x in r:
                worse.append(x)
            return worker(l, worse)

        rows = row_cleaning(self.rows)
        best, rest = worker(rows, [])
        return self.clone(best), self.clone(rest)

    def sway(self, cols=None):
        def worker(rows, worse, evals0, above=None):
            if len(rows) <= len(self.rows) ** self.the["min"]:
                return rows, many(worse, self.the['rest'] * len(rows)), evals0
            l, r, A, B, m, c, evals = self.half(rows, cols, above)
            if self.better(B, A):
                l, r, A, B = r, l, B, A
            for x in r:
                worse.append(x)
            return worker(l, worse, evals + evals0, A)

        best, rest, evals = worker(self.rows, [], 0)
        return self.clone(best), self.clone(rest), evals

    def tree(self, rows=None, min=None, cols=None, above=None):
        if not rows:
            rows = self.rows
        if not min:
            min = len(rows) ** self.the["min"]
        if not cols:
            cols = self.cols.x

        node = {"data": self.clone(rows)}
        if len(rows) > 2 * min:
            left, right, node["A"], node["B"], node["mid"], _, _ = self.half(rows, cols, above)
            node['left'] = self.tree(left, min, cols, node['A'])
            node['right'] = self.tree(right, min, cols, node['B'])

        return node

    def prune(self, rule, max_size):
        n = 0
        for txt, r in rule.items():
            n = n + 1
            if len(r) == max_size[txt]:
                n = n + 1
                rule[txt] = None
        if n > 0:
            return rule

    def RULE(self, ranges, max_size):
        t = {}
        for r in ranges:
            if r.txt not in t:
                t[r.txt] = []
            t[r.txt].append({'lo': r.lo, 'hi': r.hi, 'at': r.at})
        return self.prune(t, max_size)

    def xpln(self, best, rest):
        tmp = []
        max_size = {}

        def v(has):
            return value(has, len(best.rows), len(rest.rows), "best")

        def score(ranges):
            rule = self.RULE(ranges, max_size)
            if rule:
                print(showRule(rule))
                bestr = selects(rule, best.rows)
                restr = selects(rule, rest.rows)
                if len(bestr) + len(restr) > 0:
                    return v({'best': len(bestr), 'rest': len(restr)}), rule

        for ranges in bins(self.cols.x, {'best': best.rows, 'rest': rest.rows}, self.the):
            max_size[ranges[1].txt] = len(ranges)
            print()
            for r in ranges:
                print(r.txt, r.lo, r.hi)
                val = v(r.y.has)
                tmp.append({'range': r, 'max': len(ranges), 'val': val})
        rule, most = firstN(sorted(tmp, key=lambda x: x['val'], reverse=True), score)
        return rule, most

    def betters(self, n):
        sorted_rows = list(sorted(self.rows, key=functools.cmp_to_key(lambda x, y: -1 if self.better(x, y) else 1)))
        return sorted_rows[1:n], sorted_rows[n + 1:] if n is not None else sorted_rows
