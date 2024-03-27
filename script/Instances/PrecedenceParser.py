import os
from typing import List


# parse a precedence file (each line is "prec i j")
def parse_precedence(filename: str):
    with open(filename) as file:
        return [(int(l[1])-1, int(l[2])-1) for l in [l.strip().split() for l in file.readlines()]]


# create a file and log all the precedence in the file
def log_precedence(filename: str, prec: List[List[int]]):
    with open(filename, "w") as file:
        for (a, b) in prec:
            file.write("prec {} {}\n".format(a+1, b+1))


def parse_precedence_multi(filename: str):
    with open(filename) as file:
        lines = file.readlines()
        size = len(lines)
        idx_list = [idx for idx, val in
                    enumerate(lines) if '--' in val][1:]
        res = [lines[i+1: j] for i, j in
               zip([0] + idx_list, idx_list +
                   ([size] if idx_list[-1] != size else []))]
        res = [[(int(l[1])-1, int(l[2])-1) for l in [l.strip().split() for l in one]] for one in res]
        return res



if __name__ == "__main__":
    lines = ["-- 1 --", "1", "2", "-- 2 --", "3","4","5", "-- 3 --", "6"]
    size = len(lines)
    idx_list = [idx for idx, val in
                enumerate(lines) if '--' in val][1:]
    print(idx_list)

    res = [lines[i+1: j] for i, j in
           zip([0] + idx_list, idx_list +
               ([size] if idx_list[-1] != size else []))]
    print(res)