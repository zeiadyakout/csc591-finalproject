import re
from .num import NUM
from .sym import SYM


class COLS:
    def __init__(self, row):
        x, y, all_cols = [], [], []
        klass = None
        for at, txt in enumerate(row.cells):
            col = NUM(txt, at) if re.match("^[A-Z]", txt) else SYM(txt, at)
            all_cols.append(col)
            
            if txt.endswith("!"):
                klass = col
            if re.search("[!+-]$", txt):
                y.append(col)
            else:
                x.append(col)
        self.x, self.y, self.all, self.klass, self.names = x, y, all_cols, klass, row

    def add(self, row):
        for cols in [self.x, self.y]:
            for col in cols:
                col.add(row.cells[col.at])
        return row
