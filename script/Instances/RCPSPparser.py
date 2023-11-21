# Parser for the RCPSP instances
from script.Instances.PrecedenceParser import log_precedence
from script.Instances.RCPSPinstance import RCPSP
from script.Instances.bench import mapfctformat
import os

from script.parameters import DIR_DATAS_PICKLE, DIR_DATAS
from script.save_pickle_json import p_load, p_save_high


# parse a file containing a RCPSP instance
def parse_rcpsp(filename: str, formatting: str= "psplib"):
    basename = os.path.basename(filename)
    filename_stored = os.path.join(DIR_DATAS_PICKLE, "{}.pkl".format(basename))
    if os.path.exists(filename_stored):
        return p_load(filename_stored)
    else:
        inst = mapfctformat[formatting]["parse_rcpsp"](filename)
        p_save_high(filename_stored, inst)  # pickle instance for next time
        return inst


# log in file output_file all the trivial precedence ("prec i j")
# if a precedes b and b precedes c, a precedes c is trivial
# also called precedences by transitivity
def log_trivial_precedences(instance: RCPSP, output_file: str):
    successors = instance.successors
    all_successors = instance.all_succ
    precedences = []
    for i in range(instance.nb_jobs):
        for j in all_successors[i]:
            if j not in successors[i]:
                precedences.append([i, j])
    log_precedence(output_file, precedences)


if __name__ == "__main__":
    # inst = parse_rcpsp(os.path.join(DIR_DATAS,"j120/j1201_1.sm", PSPLIB))
    inst = parse_rcpsp(os.path.join(DIR_DATAS, "psplib/j30/j301_1.sm"))
    print(inst)
