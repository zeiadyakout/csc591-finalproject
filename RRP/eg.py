from .data import DATA
from .num import NUM
from .sym import SYM
import l
import sys
import ast
from .misc import *
import math
import random
from .config import the
from .rules import RULES

def stats(src=None):
    data = DATA(src or "../../data/auto93.csv")
    result = l.sort_string(l.o(data.stats()))
    print(f"\nStats: {result}\n")
    result_bool = result == "{.N: 398, Acc+: 15.57, Lbs-: 2970.42, Mpg+: 23.84}"
    return result_bool

def columns(src=None):
    data = DATA(src or "../../data/auto93.csv")
    expected = 8
    actual = len(data.cols.all)
    print(f"Expected number of columns in file: {expected}\nActual: {actual}\n")
    return expected == actual

def dependent(src=None):
    data = DATA(src or "../../data/auto93.csv")
    expected = 3
    actual = len(data.cols.y)
    print(f"Expected number of dependent variables in file: {expected}\nActual: {actual}\n")
    return expected == actual

def independent(src=None):
    data = DATA(src or "../../data/auto93.csv")
    expected = 4
    actual = len(data.cols.x)
    print(f"Expected number of independent variables in file: {expected}\nActual: {actual}\n")
    return expected == actual

def num_mean():
    num = NUM()
    num.add(5)
    expected = 5
    actual = num.mu
    print(f"Expected num.mean: {expected}\nActual num.mean: {actual}\n")
    return expected == actual

def num_mid():
    num = NUM()
    num.add(5)
    num.add(10)
    expected = 7.5
    actual = num.mid()
    print(f"Expected num.mid: {expected}\nActual num.mid: {actual}\n")
    return expected == actual

def num_div():
    num = NUM()
    num.add(1)
    expected = 0
    actual = num.div()
    print(f"Expected num.div: {expected}\nActual num.div: {actual}\n")
    return expected == actual

def num_like():
    num = NUM()
    num.add(15)
    num.add(25)
    expected = 0.0201
    actual = num.like(10, None)
    print(f"Expected num.like(): near .0208\nActual num.like(): {actual}\n")
    return actual - expected < .001

def sym_add():
    sym = SYM()
    sym.add("A")
    print(f"Expected sym.n: 1\nActual sym.n: {sym.n}\n")
    print(f"Expected sym.has['A']: 1\nActual sym.has['A']: {sym.has['A']}\n")
    print(f"Expected sym.mode: \"A\"\nActual sym.mode: {sym.mode}\n")
    return sym.n == 1 and sym.has['A'] == 1 and sym.mode == "A"
    
def sym_add_mul_val():
    sym = SYM()
    values = ["A", "B", "A", "C", "B", "A"]
    for value in values:
        sym.add(value)
    print(f"Expected sym.n: {len(values)}\nActual sym.n: {sym.n}\n")
    print(f"Expected sym.has[\"A\"]: 3\nActual sym.has[\"A\"]: {sym.has['A']}\n")
    print(f"Expected sym.has[\"B\"]: 2\nActual sym.has[\"B\"]: {sym.has['B']}\n")
    print(f"Expected sym.has[\"C\"]: 1\nActual sym.has[\"C\"]: {sym.has['C']}\n")
    print(f"Expected sym.mode: \"A\"\nActual sym.mode: {sym.mode}\n")
    return sym.n == len(values) and sym.has["A"] == 3 and sym.has["B"] == 2 and sym.has["C"] == 1 \
and sym.mode == 'A'

def sym_mid():
    sym = SYM()
    sym.add("A")
    expected = 0
    actual = sym.mid()
    print(f"Expected sym.mid: 0\nActual sym.mid: {actual}")
    return expected == actual

def sym_like():
    sym = SYM()
    sym.add("A")
    sym.add("B")
    sym.add("C")
    sym.add("D")
    sym.add("E")
    expected = .2286
    actual = sym.like("B", .3)
    print (f"Expected sym.like(): .2286\nActual sym.like(): {actual}\n")
    return actual - expected < .0001

def learn(data, row, my):
    my["n"] = my["n"] + 1
    kl = row.cells[data.cols.klass.at]
    if my["n"] > 10:
        my["tries"] += 1
        my["acc"] = my["acc"] + (1 if kl == row.likes(my["datas"]) else 0)
    
    if kl not in my["datas"]: my['datas'][kl] = DATA(data.cols.names)
    my['datas'][kl].add(row)

def bayes():
    wme = {"acc": 0, "datas": {}, "tries": 0, "n": 0}
    DATA("../../data/diabetes.csv", lambda data, t: learn(data, t, wme))
    print(wme["acc"]/wme["tries"])
    return wme["acc"]/wme["tries"] > .72

def km():
    print("#%4s\t%s\t%s" % ("acc", "k", "m"))
    k_values = [0, 1, 2, 3]
    m_values = [0, 1, 2, 3]
    for k in k_values:
        for m in m_values:
            the["k"] = k
            the["m"] = m
            wme = {"acc": 0, "datas": {}, "tries": 0, "n": 0}
            DATA("../../data/soybean.csv", lambda data, t: learn(data, t, wme))
            print("%5.2f\t\%s\t\%s" % (wme["acc"]/wme["tries"], k, m))

def sorted(src=None):
    print("Sorted: ")
    dataset = DATA(src or "../../data/auto93.csv")
    firstRow = dataset.rows[0]
    neighbors = firstRow.neighbors(dataset)

    for i, row in enumerate(neighbors):
        if i % 30 == 0:
            print(f"{(i+1): <8} {row.cells} {firstRow.dist(row, dataset):10.2f}")
    
def far(src=None):
    print("Far: ")
    dataset = DATA(src or "../../data/auto93.csv")

    a, b, C, evals = dataset.farapart(dataset.rows)
    print("far1: ", a.cells)
    print("far2: ", b.cells)
    print(f"distance = {C:.2f}")
    print("Evaluations: ", evals)
    
def half(src=None):
    dataset = DATA(src or "../../data/auto93.csv")
    lefts, rights, left, right, C, cut = dataset.half(dataset.rows)
    o = l.o
    print(o(len(lefts)), o(len(rights)), o(left.cells), o(right.cells), o(C), o(cut))

def tree(src=None):
    t, evals = DATA(src or "../../data/auto93.csv").tree(True)
    t.show()
    print(evals)

def branch(src=None):
    dataset = DATA(src or "../../data/auto93.csv")
    best, rest, evals = dataset.branch()
    print(l.o(best.mid().cells), l.o(rest.mid().cells))
    print(evals)

def doubletap(src=None):
    dataset = DATA(src or "../../data/auto93.csv")
    best1, rest, evals1 = dataset.branch(32)
    best2, _, evals2 = best1.branch(4)
    print(l.o(best2.mid().cells), l.o(rest.mid().cells))
    print(evals1+evals2)

def bins(src=None):
    dataset = DATA(src or "../../data/auto93.csv")
    best, rest = dataset.branch()#[:2]
    like = best.rows
    hate = l.slice(l.shuffle(rest.rows), 1, 3 * len(like))
    def score(range):
        return range.score("like", len(like), len(hate))
    t = []
    for _, col in enumerate(dataset.cols.x):
        print(col)
        print()
        for range in _ranges1(dataset.cols.all[col], {"LIKE":like, "HATE":hate}):
            l.oo(range)
            t.append(range)
    t = sorted(t, key=lambda x: score(x), reverse=True)
    max = score(t[0])
    print("\n#scores:\n")
    for v in l.slice(t, 1, the["B"]):
        if score(v) > max * 0.1:
            print(l.rnd(score(v)), l.o(v))
    l.oo({"LIKE":len(like), "HATE":len(hate)})

def rules(src=None):
    dataset = DATA(src or "../../data/auto93.csv")

    tmp = l.shuffle(dataset.rows)
    train = dataset.clone(l.slice(tmp, 1, len(tmp)//2))
    test = dataset.clone(l.slice(tmp, len(tmp)//2 + 1))
    best0, rest, evals1 = train.branch(the.d)
    best, _, evals2 = best0.branch(the.D)
    print(evals1+evals2+the.D-1)

    LIKE = best.rows
    HATE = l.slice(l.shuffle(rest.rows), 1, 3 * len(LIKE))
    rowss = {"LIKE": LIKE, "HATE": HATE}

    print(f'{"Score":^10} {"Mid Selected":^60} {"Rule":^30}')
    print("__________ ____________________________________________________________ ______________________________")
    for rule in RULES(_ranges(dataset.cols.x, rowss), "LIKE", rowss).sorted:
        result = train.clone(rule.selects(test.rows))
        if len(result.rows) > 0:
            result.rows.sort(key=lambda row: row.d2h(dataset))
            # print(round(rule.scored, 2), "\t", [round(float(value), 2) for value in result.mid().cells], "\t", rule.show())
            print(f'{round(rule.scored, 2):<10}', [round(float(value), 2) for value in result.mid().cells], f'{rule.show():>50}')



    


def run_test(test_name):
    if test_name == "stats":
        return stats()
    if test_name == "columns":
        return columns()
    if test_name == "dependent":
        return dependent()
    if test_name == "independent":
        return independent()
    if test_name == "num_mean":
        return num_mean()
    if test_name == "num_div":
        return num_div()
    if test_name == "num_mid":
        return num_mid()
    if test_name == "num_like":
        return num_like()
    if test_name == "sym_mid":
        return sym_mid()
    if test_name == "sym_add":
        return sym_add()
    if test_name == "sym_add_mul_val":
        return sym_add_mul_val()
    if test_name == "sym_like":
        return sym_like()
    if test_name == "bayes":
        return bayes()
    if test_name == "km":
        return km()
    

def all(bad=0):
    bad = 0
    for k in l.keys(globals()):
        if k != "all":
            if run_test(k) == False:
                bad += 1
        
    sys.stderr.write(f"{'❌ FAIL' if bad > 0 else '✅ PASS'} {bad} fail(s) \n")
    sys.exit(bad)

def sym():
    sym = SYM()
    for x in [1, 1, 1, 1, 2, 2, 3]:
        sym.add(x)
    mode, e = sym.mid(), sym.div()
    print(mode, e)
    return 1.37 < e and e < 1.38 and mode == 1

def norm(mu=0, sd=1):
    r = random.random()
    return mu + sd * math.sqrt(-2 * math.log(r)) * math.cos(2 * math.pi * r)

def num():
    num = NUM()
    for _ in range(1, 1000): num.add(norm(10, 2))

    mu, sd = num.mid(), num.div()

    print(l.rnd(mu, 3), l.rnd(sd, 3))
    return 10 < mu and mu < 10.1 and 2 < sd and sd < 2.05

def data():
    dataset = DATA("../../data/diabetes.csv")
    n=0

    for i, row in enumerate(dataset.rows):
        if i % 100 == 0:
            n += len(row.cells)
            l.oo(row.cells)
            print(n)
    return n == 63

def dist(src=None):
    dataset = DATA(src or "../../data/auto93.csv")
    r1 = dataset.rows[0]
    rows = r1.neighbors(dataset)

    for i, row, in enumerate(rows):
        if i % 30 == 0:
            print(l.o(row.cells), l.rnd(row.dist(r1, dataset)))

def far(src=None):
    dataset = DATA(src or "../../data/auto93.csv")
    a, b, C, evals = dataset.farapart(dataset.rows)
    print(a.cells, b.cells, C)
   

random.seed(the.seed)
#half()