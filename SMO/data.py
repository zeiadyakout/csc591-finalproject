from row import ROW
from cols import COLS
import csv
import l
import random


class DATA:
    def __init__(self, src, fun=None):
        self.rows = []
        self.cols = None

        if isinstance(src, str):
            with open(src, "r") as input_data:
                csv_reader = csv.reader(input_data)
                for x in csv_reader:
                    self.add(x, fun)

        else:
            if src:
                self.add(src, fun)
            else:
                self.add({}, fun)

    def add(self, t, fun=None, row=None):
        row = t if hasattr(t, 'cells') else ROW(t)

        if self.cols:
            if fun:
                fun(self, row)

            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        u = []

        for _, col in cols.items() if cols else self.cols.all.items():
            u.append(col.mid())

        return ROW(u)

    def div(self, cols=None):
        u = []

        for _, col in cols.items() if cols else self.cols.all.items():
            u.append(col.div())

        return ROW(u)

    def small(self):
        u = []

        for col in self.cols.all.items():
            u.append(col.small())

        return ROW(u)
    
    def stats(self, cols='y', fun='mid', ndivs=2, u={}):
        u = {".N": len(self.rows)}
        for _, col in self.cols.all.items():
            if cols == 'y' or (cols and col.txt == cols):
                value = getattr(col, fun or "mid", lambda x: x.mid)()
                u[col.txt] = l.rnd(value, ndivs)
        filtered_cols = {key: value for key, value in u.items() if key.endswith(
            '!') or key.endswith('+') or key.endswith('-') or key == ".N"}
        return filtered_cols

    def gate(self, budget0, budget, some):
        stats, bests = [], []

        self.rows = l.shuffle(self.rows)
        
        top6 = self.rows[:6]
        # print("1. top6")
        # for row in top6:
        #     print(row.cells)
        # print()
        
        top50 = self.rows[:50]
        # print("2. top50")
        # for row in top50:
        #     print(row.cells)
        # print()
        # Not working past this point

        rows_d2h = []
        for row in self.rows:
            rows_d2h.append((row.d2h(data=DATA("../../data/auto93.csv")), row))
        rows_d2h = sorted(rows_d2h, key = lambda x: x[0])
        # print("3. most", rows_d2h[0][1].cells, "\n")

        rows = l.shuffle(self.rows)
        lite = rows[:budget0+1] #l.slice(rows, 1, budget0)

        dark = rows[budget0+1:] #l.slice(rows, budget0+1) # We'll need to adjust the parameter in the function definition of slice()

        rows4 = []
        rows5 = []
        rows6 = []
        
        for i in range(budget): #Using +1 to include all values in budget
            lite_d2h = []
            for row in lite:
                lite_d2h.append((row.d2h(data=DATA("../../data/auto93.csv")), row))
            lite_d2h = sorted(lite_d2h, key = lambda x: x[0])
            best, rest = self.bestRest(lite, len(lite) ** some)
            todo, selected = self.split(best, rest, lite, dark)
            stats.append(selected.mid())
            bests.append(best.rows[0]) #Lua lists are indexed starting at 1, python is 0
            # print("4: rand")
            rand_rows = random.sample(dark, budget0)
            for row in rand_rows:
                # print(row.cells)
                rows4.append(row)
                

            # print("5: mid\n", selected.mid().cells)
            rows5.append(selected.mid())

            # print("6: top\n", bests[-1].cells)
            rows6.append(bests[-1])
            lite.append(dark.pop(todo))
        
        # print("4: rand")
        # for row in rows4:
        #     print(row.cells)
        # print()
        
        # print("5: mid")
        # for row in rows5:
        #     print(row.cells)
        # print()

        # print("6: top")
        # for row in rows6:
        #     print(row.cells)
        # print()
        
        return stats, bests
    

    def split(self, best, rest, lite, dark):
        selected = DATA(self.cols.names)
        max = 1E30
        out = 1

        for i, row in enumerate(dark):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            
            if b > r:
                selected.add(row)
            
            tmp = abs(b + r) / abs(b - r + 1E-300)

            if tmp > max:
                out, max = i, tmp

        return out, selected

    def bestRest(self, rows, want, best=None, rest=None, top=None):
        rows.sort(key = lambda row: row.d2h(self))

        best, rest = DATA(self.cols.names), DATA(self.cols.names)

        for i, row in enumerate(rows):
            if i <= want:
                best.add(row)
            else:
                rest.add(row)
        
        # print("Best: ", len(best))
        # print("Rest: ", len(rest))
        return best, rest