from config import the
import math

class NUM:

    # Create
    def __init__(self, s=" ", n=0):

        self.txt = s
        self.at = n
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = -1E30
        self.lo = 1E30
        self.heaven = 0 if s.startswith("-") else 1

    # Update
    def add(self, x):
        if x != "?":
            self.n = self.n+1
            d = float(x) - self.mu
            self.mu += d/self.n
            self.m2 += d*(float(x) - self.mu)
            self.lo = min(float(x), self.lo)
            self.hi = max(float(x), self.hi)

    # Query
    def mid(self):
        return self.mu

    def div(self):
        return 0 if self.n < 2 else (self.m2/(self.n - 1))**0.5

    def small(self):
        return the.cohen * self.div()

    def norm(self, x):
        return x if x == "?" else (float(x) - self.lo)/(self.hi - self.lo + 1E-30)

    def dist(self, x, y):
        if x == "?" and y == "?":
            return 1
        x, y = self.norm(x), self.norm(y)
        if x == "?":
            x = 1 if y < .5 else 0
        if y == "?":
            y = 1 if x < .5 else 0
        return abs(x - y)
    
    def bin(self, x):
        tmp = (self.hi - self.lo) / (the.bins - 1)
        return 1 if self.hi == self.lo else math.floor(float(x) / tmp + .5) * tmp
    
    # Likelihood
    def like(self, x, _):
        mu, sd = self.mid(), (self.div() + 1E-30)
        nom = 2.718**(-0.5 * (float(x) - mu)**2 / (sd ** 2))
        denom = (sd * 2.5 + 1E-30)
        return nom/denom
