from config import the
import math
import cols

class ROW:
    def __init__(self, t):
        self.cells = t

    def d2h(self, data, d=None, n=None):
        d, n = 0, 0
        for col in data.cols.y.values():
            #print(type(self.cells[col.at]))
            n += 1
            d = d + abs(col.heaven - col.norm(float(self.cells[col.at]))) ** 2
        return d ** .5 / n ** .5
    
    def likes(self, datas, most=None): 
        n, nHypotheses = 0, 0
        for k, data in datas.items():
            n += len(data.rows)
            nHypotheses += 1
        for k, data in datas.items():
            tmp = self.like(data, n, nHypotheses)
            if most == None or tmp > most:
                most, out = tmp, k
        return out
    
    def like(self, data, n, nHypotheses): 
        prior = (len(data.rows) + the.k) / (n + the.k * nHypotheses)
        out = math.log(prior)
        for col in data.cols.x.values():
            v = self.cells[col.at]
            if v != '?':
                inc  = col.like(v, prior)
                if(inc > 0):
                    out += math.log(inc)
        return math.exp(1) ** out