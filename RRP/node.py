from RRP.l import *

class NODE:
    def __init__(self, data):
        self.here = data
        self.lefts = None
        self.rights = None
    
    def walk(self, fun, depth=0):
        fun(self, depth, not (self.lefts or self.rights))
        if self.lefts:
            self.lefts.walk(fun, depth + 1)
        if self.rights:
            self.rights.walk(fun, depth + 1)

    def show(self, _show=None, maxDepth=None):
        def d2h(data):
            return rnd(data.mid().d2h(self.here))
        
        maxDepth = 0

        def _show(node, depth, leafp, post=None):
            nonlocal maxDepth
            post = f"{d2h(node.here)}\t{o([f'{cell:.2f}' for cell in node.here.mid().cells])}" if leafp else "" # This is a mess, but might be correct?
            maxDepth = max(maxDepth, depth)
            print("|.. " * depth + post)
        
        self.walk(_show)
        print("")
        print("    " * maxDepth + str(d2h(self.here)) + str(o([f'{cell:.2f}' for cell in self.here.mid().cells])))
        print("    " * maxDepth + "_" + str(o(self.here.cols.names)))
        
