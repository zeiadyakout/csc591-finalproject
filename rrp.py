from RRP.config import *
from data import DATA
from RRP.eg import *

def rrp():
    data = DATA("data/wineQuality/wineQuality.csv")
    node, evals = data.tree(True)
    node.show()
    print("evals: ", evals)

doubletap()
rrp()