"""
gate: guess, assess, try, expand
(c) 2023, Tim Menzies, BSD−2
Learn a little, guess a lot, try the strangest guess, learn a little more, repeat

USAGE:
python gate.py [OPTIONS]

OPTIONS:
-c --cohen small effect size = .35
-f --file csv data file name = ../data/diabetes.csv
-h --help show help = false
-k --k low class frequency kludge = 1
-m --m low attribute frequency kludge = 2
-s --seed random number seed = 23408
-t --todo start up action = help
"""

import argparse, re, ast

# b4 = {}
# for k, _ in globals().items():
#     b4[k] = k

l = []
the = {}

def parse_args():
    parser = argparse.ArgumentParser(
        description="Read CSV and print statistics")
    parser.add_argument(
        "-c", "--cohen", help='small effect size', required=False, default=0.35)
    parser.add_argument("-f", "--file", help="CSV data file name",
                        required=False, default="../data/diabetes.csv")
    parser.add_argument("-H", "--Help", help="show help",
                        required=False, default=False)
    parser.add_argument(
        "-k", "--k", help="low class frequency kludge", required=False, default=1)
    parser.add_argument(
        "-m", "--m", help="low attribute frequency kludge", required=False, default=2)
    parser.add_argument("-s", "--seed", help="random number seed",
                        required=False, default=23408, type=int)
    parser.add_argument(
        "-t", "--type", help="start up action (e.g., 'stats', 'all')", required=False, default="help")

    args = parser.parse_args()

    return args

# The below code was imported from tricks.py, as provided by Dr. Menzies
def coerce(x):
   try : return ast.literal_eval(x)
   except Exception: return x.strip()

def oo(x) : print(o(x)); return x

def o(x): 
  return x.__class__.__name__ +"{"+ (" ".join([f":{k} {v}" for k,v in sorted(x.items())
                                                           if k[0]!="_"]))+"}"

class SLOTS(dict): 
  __getattr__ = dict.get; __setattr__ = dict.__setitem__; __repr__ = o

the = SLOTS(**{m[1]:coerce(m[2]) for m in re.finditer( r"--(\w+)[^=]*=\s*(\S+)",__doc__)})