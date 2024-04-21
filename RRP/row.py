from .config import the
import math
import cols
import sys
from .l import *

class ROW:
    def __init__(self, t):
        self.cells = t

    def d2h(self, data):
        d, n, p = 0, 0, 2

        for col in data.cols.y:
            n += 1
            d += math.pow(abs(col.heaven - col.norm(self.cells[col.at])), p)

        return math.pow(d / n, 1 / p)
        
    def dist(self, other, data):
        d, n, p = 0, 0, the.p
        for col in data.cols.x:
            n += 1
            d += col.dist(self.cells[col.at], other.cells[col.at]) ** p
        return math.pow(d / n, 1 / p)
    
    def neighbors(self, data, rows=None):
        if rows is None:
            rows = data.rows
        return keysort(rows, lambda row: self.dist(row, data))
    
