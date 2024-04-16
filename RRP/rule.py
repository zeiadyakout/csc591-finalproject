class RULE:
    def __init__(self, ranges):
        self.parts = {}
        self.scored = 0
        rule = self
        for range_ in ranges:
            t = rule.parts.get(range_.txt, [])
            t.append(range_)
            rule.parts[range_.txt] = t

    def _or(self, ranges, row, x=None, lo=None, hi=None):
        x = row.cells[ranges[0].at]
        if x == "?":
            return True
        for range_ in ranges:
            lo, hi = range_.x['lo'], range_.x['hi']
            if float(lo) == float(hi) and float(lo) == float(x) or float(lo) <= float(x) < float(hi):
                return True
        return False
    
    def _and(self, row):
        for ranges in self.parts.values():
            if not self._or(ranges, row):
                return False
        return True
    
    def selects(self, rows):
        t = []
        for r in rows:
            if self._and(r):
                t.append(r)
        return t
    
    def selectss(self, rowss, t=None):
        t = {}
        for y, rows in rowss.items():
            t[y] = len(self.selects(rows))
        return t
    
    def show(self, ands=None):
        if ands is None:
            ands = []
        for ranges in self.parts.values():
            ors = _showLess(ranges)
            at = None # Never actually use this...
            for i, range_ in enumerate(ors):
                at = range_.at # This either...
                ors[i] = range_.show()
            ands.append(" or ".join(ors))
        return " and ".join(ands)

def _showLess(t, ready=False):
    if not ready:
        t.sort(key=lambda a: float(a.x['lo']))
    
    i, u = 0, []
    while i < len(t):
        a = t[i]
        if i < len(t) - 1 and a.x['hi'] == t[i + 1].x['lo']:
            a = a.merge(t[i + 1])
            i += 1
        u.append(a)
        i += 1
    
    return t if len(u) == len(t) else _showLess(u, True)
    