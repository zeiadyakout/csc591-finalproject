import math
from .config import the
from .l import *

class SYM:
    def __init__(self, s=" ", n=0):
        self.txt = s
        self.at = n
        self.n = 0
        self.has = {}
        self.mode = None
        self.most = 0
    
    def add(self, x):
        if x != "?":
            self.n += 1
            self.has[x] = self.has.get(x, 0) + 1

            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x
    
    def mid(self):
        return self.mode
    
    def div(self):
        e = 0
        for v in self.has.values():
            e -= v / self.n * math.log(v / self.n, 2)

        return e
    
    def small(self):
        return 0
    
    def norm(self, x):
        return x
    
    def dist(self, x, y):
        return 1 if (x == "?" and y == "?") else 0 if x == y else 1
    
    def bin(self, x):
        return x
    
    def like(self, x, prior):
        if self.n + self.the.m == 0:
            return 0
        
        return ((self.has.get(x, 0) or 0) + the.m * prior) / (self.n + the.m)