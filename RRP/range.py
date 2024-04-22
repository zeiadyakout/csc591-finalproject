from RRP.l import *

class RANGE:
    def __init__(self, at, txt, lo, hi=None):
        self.at = at
        self.txt = txt
        self.scored = 0
        self.x = {'lo': lo, 'hi': hi or lo}
        self.y = {}

    def add(self, x, y):
        self.x['lo'] = min(self.x['lo'], x)
        self.x['hi'] = max(self.x['hi'], x)
        self.y[y] = (self.y.get(y, 0)) + 1

    def show(self, lo=None, hi=None, s=None):
        lo, hi, s = self.x['lo'], self.x['hi'], self.txt
        if lo == '-inf':
            return f"{s} < {hi}"
        if hi == 'inf':
            return f"{s} >= {lo}"
        if lo == hi:
            return f"{s} == {lo}"
        return f"lo <= {s} < {hi}"
    
    def range_score(self, goal, LIKE, HATE):
        return l_score(self.y, goal, LIKE, HATE)
    
    def merge(self, other):
        both = RANGE(self.at, self.txt, self.x['lo'])
        both.x['lo'] = min(self.x['lo'], other.x['lo'])
        both.x['hi'] = max(self.x['hi'], other.x['hi'])
        for t in [self.y, other.y]:
            for k, v in t.items():
                both.y[k] = (both.y.get(k, 0) + v)
        return both

    def merged(self, other, tooFew):
        both = self.merge(other)
        e1, n1 = entropy(self.y)
        e2, n2 = entropy(other.y)
        if n1 <= tooFew or n2 <= tooFew:
            return both
        e, _ = entropy(both.y)
        if e <= (n1 * e1 + n2 * e2) / (n1 + n2):
            return both
    