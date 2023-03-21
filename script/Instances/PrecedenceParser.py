import os
from typing import List

from script.parameters import DIR_PROJECT, DIR_PREPROCESSED


# parse a precedence file (each line is "prec i j")
def parse_precedence(filename: str):
    with open(filename) as file:
        return [(int(l[1])-1, int(l[2])-1) for l in [l.strip().split() for l in file.readlines()]]


# create a file and log all the precedence in the file
def log_precedence(filename: str, prec: List[List[int]]):
    with open(filename, "w") as file:
        for (a, b) in prec:
            file.write("prec {} {}\n".format(a+1, b+1))
