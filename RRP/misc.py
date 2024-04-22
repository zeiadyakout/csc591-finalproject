from RRP.range import RANGE
from RRP.l import *
from RRP.config import *

def _ranges(cols, rowss):
    t = []
    for col in cols:
        for range in _ranges1(col, rowss):
            t.append(range)
    return t

def _ranges1(col, rowss):
    out, nrows = {}, 0
    for y, rows in rowss.items():
        nrows += len(rows)
        for row in rows:
            x = row.cells[col.at]
            if x != '?':
                bin = col.bin(x)
                if bin not in out:
                    out[bin] = RANGE(col.at, col.txt, x)
                out[bin].add(x, y)
    out = list(out.values())
    out.sort(key=lambda a: a.x['lo'])

    return out if hasattr(col, 'has') else _mergeds(out, nrows // the.bins)

def _mergeds(ranges, tooFew):
    i, t = 0, []
    while i < len(ranges):
        a = ranges[i]
        if i < len(ranges) - 1:
            both = a.merged(ranges[i+1], tooFew)
            if both:
                a = both
                i += 1
        t.append(a)
        i += 1

    if len(t) < len(ranges):
        return _mergeds(t, tooFew)
    
    for i in range(2, len(t)):
        t[i].x['lo'] = t[i - 1].x['hi']
    
    t[0].x['lo'] = float('-inf') # Error here!
    t[-1].x['hi'] = float('inf')
    return t