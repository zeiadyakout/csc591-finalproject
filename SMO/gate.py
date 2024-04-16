from config import parse_args, the
from data import DATA
import eg
import os
import shutil
import sys

if __name__ == "__main__":
    args = parse_args()

    if args.type == "stats":
        stats_result = eg.stats()

    elif args.type == "all":
        eg.all()

    if args.type == "independent":
        independent_result = eg.independent()

    elif args.type == "columns":
        columns_result = eg.columns()

    elif args.type == "dependent":
        dependent_result = eg.dependent()

    elif args.type == "num_mid":
        num_mid_result = eg.num_mid()

    elif args.type == "num_mean":
        num_mean_result = eg.num_mean()

    elif args.type == "num_div":
        num_div_result = eg.num_div()

    elif args.type == "sym_add":
        sym_div_result = eg.sym_add()
    
    elif args.type == "sym_add_mul_val":
        sym_add_mul_val_result = eg.sym_add_mul_val()

    elif args.type == "sym_mid":
        sym_mid_result = eg.sym_mid()

    elif args.type == "bayes":
        bayes_result = eg.bayes()

    elif args.type == "km":
        km_result = eg.km()