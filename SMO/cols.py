import re
from num import NUM
from sym import SYM


class COLS:
    def __init__(self, row):
        x, y, all_cols = {}, {}, {}
        klass, col = None, None
        for at, txt in enumerate(row.cells):
            col = NUM(txt, at) if re.match("^[A-Z]", txt) else SYM(txt, at)
            all_cols[at] = col
            if not txt.endswith("$"):
                if txt.endswith("!"):
                    klass = col
                if re.search("[!+-]$", txt):
                    y[at] = col
                elif not txt.endswith("X") and not re.search("[!+-]$", txt):
                    x[at] = col
        self.x, self.y, self.all, self.klass, self.names = x, y, all_cols, klass, row.cells

    def add(self, row):
        for cols in [self.x, self.y]:
            for _, col in cols.items():
                col.add(row.cells[col.at])
        return row