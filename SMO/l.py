import math
import ast
import random

def keys(t, u=None):
    if u is None:
        u = []
    for k in sorted(t.keys()):
        u.append(k)
    return u

def rnd(n, ndecs):
    if isinstance(n, int):
        return n
    if math.floor(n) == n:
        return n
    mult = 10 ** (ndecs or 2)
    return math.floor(n * mult + 0.5) / mult

def o(t, n=2, u=None):
    if isinstance(t, (int, float)):
        return str(rnd(t, n))
    if not isinstance(t, dict):
        return str(t)
    
    if u is None:
        u = []
    
    for k in [key for key in t.keys() if str(key)[0] != '_']:
        if isinstance(t[k], dict):
            if len(t[k]) > 0:
                u.append(o(t[k], n))
            else:
                u.append(f"'{o(k, n)}': {o(t[k], n)}")
        else:
            u.append(f"'{o(k, n)}': {o(t[k], n)}")

    return "{" + ", ".join(u) + "}"

def shuffle(t):
    u = t.copy()
    random.shuffle(u)
    return u
# def shuffle(t, j):
#     u = []
#     for x in t.values():
#         u.append(x)
    
#     for i in range(len(u) - 1, 0, -1):
#         j = random.randint(0, i) # Unsure if these are the correct bounds
#         u[i], u[j] = u[j], u[i]
    
#     return u

def slice(t, go=None, stop=None, inc=None):
    if go is not None and go < 0:
        go += len(t)
    
    if stop is not None and stop < 0:
        stop += len(t)

    u = []

    go = int(go) if go is not None else 1
    stop = int(stop) if stop is not None else len(t)
    inc = int(inc) if inc is not None else 1

    for j in range(go, stop, inc):
        u.append(t[j])

    return u
    
        

def sort_string(input_string):
    input_dict = ast.literal_eval(input_string)
    sorted_dict = dict(sorted(input_dict.items()))
    output_string = str(sorted_dict).replace("'","")
    return output_string