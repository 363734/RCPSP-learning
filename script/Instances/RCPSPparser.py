# Parser for the RCPSP instances
from script.Instances.PrecedenceParser import log_precedence
from script.Instances.RCPSPinstance import RCPSP
import os

from script.parameters import DIR_DATAS_SAVE, DIR_DATAS
from script.save_pickle_json import p_load, p_save_high

PSPLIB = "psplib"


# parse a file containing a RCPSP instance
def parse_rcpsp(filename: str, formatting: str = PSPLIB):
    basename = os.path.basename(filename)
    filename_stored = os.path.join(DIR_DATAS_SAVE, "{}.pkl".format(basename))
    if os.path.exists(filename_stored):
        return p_load(filename_stored)
    else:
        if formatting == PSPLIB:
            inst = parse_rcpsp_psplib(filename)
            p_save_high(filename_stored, inst)
            return inst
        else:
            print("Format {} is not supported for the RCPSP instance".format(formatting))


# parse a file containing a RCPSP instance using the PSPLIB format
def parse_rcpsp_psplib(filename: str):
    with open(filename) as file:
        lines = file.readlines()
        nb_jobs = int(lines[5].split()[-1])
        successor = [[int(k) - 1 for k in line.strip().split()][3:] for line in lines[18:18 + nb_jobs]]
        info = [[int(k) for k in line.strip().split()][2:] for line in lines[18 + nb_jobs + 4:18 + 2 * nb_jobs + 4]]
        duration = [line[0] for line in info]
        usage = [line[1:] for line in info]
        resource = [int(k) for k in lines[-2].strip().split()]
        return RCPSP(nb_jobs, successor, duration, usage, resource)


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
    inst = parse_rcpsp(os.path.join(DIR_DATAS, "j30/j301_1.sm"))
    print(inst)
