from RRP.row import ROW
from RRP.cols import COLS
import csv
from RRP.l import *
import random
from RRP.config import *
from RRP.node import NODE


class DATA:
    def __init__(self, src, fun=None):
        self.rows = []
        self.cols = None

        if isinstance(src, str):
            with open(src, "r") as input_data:
                csv_reader = csv.reader(input_data)
                for x in csv_reader:
                    self.add(x, fun)

        else:
            if src:
                self.add(src, fun)
            else:
                self.add([], fun)

    def add(self, t, fun=None, row=None):
        row = t if hasattr(t, 'cells') else ROW(t)

        if self.cols:
            if fun:
                fun(self, row)

            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        u = []

        for col in cols or self.cols.all:
            u.append(col.mid())

        return ROW(u)

    def div(self, cols=None):
        u = []

        for col in cols or self.cols.all:
            u.append(col.div())

        return ROW(u)

    def small(self):
        u = []

        for col in self.cols.all:
            u.append(col.small())

        return ROW(u)
    
    def stats(self, cols='y', fun='mid', ndivs=2, u={}):
        u = {".N": len(self.rows)}
        for col in self.cols.all:
            if cols == 'y' or (cols and col.txt == cols):
                value = getattr(col, fun or "mid", lambda x: x.mid)()
                u[col.txt] = rnd(value, ndivs)
        filtered_cols = {key: value for key, value in u.items() if key.endswith(
            '!') or key.endswith('+') or key.endswith('-') or key == ".N"}
        return filtered_cols
    
    def clone(self, rows):
        new = DATA(self.cols.names)
        for row in rows or []:
            new.add(row)
        return new
    
    def farapart(self, rows, sortp=None, a=None, b=None, far=None, evals=None):
        far = int(len(rows) * the.Far)
        evals = 1 if a else 2
        a = any(rows).neighbors(self, rows)[far]
        b = a.neighbors(self, rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a, b = b, a

        return a, b, a.dist(b, self), evals
    
    def half(self, rows, sortp=None, before=None, evals=None):
        some = many(rows, min(the.Half, len(rows)))
        a, b, C, evals = self.farapart(some, sortp, before)
        def d(row1, row2):
            return row1.dist(row2, self)
        def project(r):
            return (d(r, a) ** 2 + C ** 2 - d(r, b) ** 2) / (2 * C)
        as_, bs = [], []
        for n, row in enumerate(keysort(rows, project)):
            if n < (len(rows) // 2 - 1):
                as_.append(row)
            else:
                bs.append(row)
        return as_, bs, a, b, C, d(a, bs[0]), evals
    
    def tree(self, sortp):
        evals = 0
        def _tree(data, above=None):
            nonlocal evals
            node = NODE(data)
            if len(data.rows) > 2 * (len(self.rows) ** 0.5):
                lefts, rights, node.left, node.right, node.C, node.cut, evals1 = self.half(data.rows, sortp, above)
                evals += evals1
                node.lefts = _tree(self.clone(lefts), node.left)
                node.rights = _tree(self.clone(rights), node.right)
            return node
        return _tree(self), evals        

    def branch(self, stop=None, rest=None, _branch=None, evals=None):
        evals, rest = 1, []
        stop = stop or (2 * (len(self.rows) ** 0.5))

        def _branch(data, above=None, left=None, lefts=None, rights=None):
            nonlocal evals
            if len(data.rows) > stop:
                lefts, rights, left, _, _, _, _= self.half(data.rows, True, above)
                evals += 1
                rest.extend(rights)
                return _branch(data.clone(lefts), left)
            else:
                return self.clone(data.rows), self.clone(rest), evals
        return _branch(self)