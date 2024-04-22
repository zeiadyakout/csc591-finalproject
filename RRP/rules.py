from RRP.l import *
from RRP.rule import RULE
from RRP.config import *

class RULES:
    def __init__(self, ranges, goal, rowss):
        self.sorted = []
        self.goal = goal
        self.rowss = rowss
        self.LIKE = 0
        self.HATE = 0

        self.likeHate()

        for range_ in ranges:
            range_.scored = self.score(range_.y)

        self.sorted = self.top(self._try(self.top(ranges)))

    def likeHate(self):
        for y, rows in self.rowss.items():
            if y == self.goal:
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        return l_score(t, self.goal, self.LIKE, self.HATE)
    
    def _try(self, ranges):
        u = []
        
        for subset in powerset(ranges):
            if len(subset) > 0:
                rule = RULE(subset)
                rule.scored = self.score(rule.selectss(self.rowss))
                if rule.scored > 0.01:
                    u.append(rule)
        
        return u
    
    def top(self, t):
        t.sort(key=lambda x: x.scored, reverse=True)
        u = []
        for x in t:
            if float(x.scored) >= float(t[0].scored) * float(the.Cut):
                u.append(x)
        return u[:the.Beam]