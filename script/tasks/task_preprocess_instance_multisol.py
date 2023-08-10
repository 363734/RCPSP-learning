import math
import os

from script.parameters import DIR_PREPROCESSED


def read_opti(bench: str, name: str, time_out_bsf: int, sbps: bool, vsids: bool, time_out_add:int):
    m = {True: "true", False: "false"}
    res_file = os.path.join(DIR_PREPROCESSED, "{}/{}_run_TO={}_sbps={}_vsids={}.txt".format(
        bench, name, time_out_bsf, m[sbps], m[vsids]))
    bsf = math.inf
    with open(res_file) as file:
        # print("reading stuff")
        lines = file.readlines()
        for k in range(len(lines)).__reversed__():
            if lines[k][:10] == "makespan =":
                bsf = int(lines[k][10:])
                break

    

