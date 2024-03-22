import os
import sys
import time

os.environ["DO_SKIP_MZN_CHECK"] = "1"

from discrete_optimization.rcpsp.rcpsp_model import RCPSPSolution
from discrete_optimization.rcpsp.rcpsp_parser import parse_file

from script.Instances.benchPSPLIB import PSPLIB, from_bench
from script.parameters import DIR_DATAS, DIR_PREDICTIONS


def read_perm(file):
    with open(file) as f:
        return [int(k)-2 for k in f.readline().strip().split()]


if __name__ == "__main__":

    psplib_name = sys.argv[1]
    model = sys.argv[2]
    threashold = sys.argv[3]
    t = time.time()
    psplib_file = os.path.join(DIR_DATAS, PSPLIB, from_bench(psplib_name), "{}.sm".format(psplib_name))
    ordering_file = os.path.join(DIR_PREDICTIONS, model, "orde_{}_{}_[{}].txt".format(psplib_name, threashold, model))
    permutation = read_perm(ordering_file)
    print(permutation)
    rcpsp_model = parse_file(psplib_file)
    mode_list = [1 for i in range(rcpsp_model.n_jobs)]
    rcpsp_sol = RCPSPSolution(
        problem=rcpsp_model, rcpsp_permutation=permutation, rcpsp_modes=mode_list
    )
    print("time : ", time.time()-t)
    print("schedule feasible: ", rcpsp_sol.rcpsp_schedule_feasible)
    print("schedule: ", rcpsp_sol.rcpsp_schedule)
    print("rcpsp_modes:", rcpsp_sol.rcpsp_modes)
    fitnesses = rcpsp_model.evaluate(rcpsp_sol)
    print("fitnesses: ", fitnesses)
    resource_consumption = rcpsp_model.compute_resource_consumption(rcpsp_sol)
    print("resource_consumption: ", resource_consumption)
    print("mean_resource_reserve:", rcpsp_sol.compute_mean_resource_reserve())
    print("makespan =",rcpsp_sol.rcpsp_schedule[rcpsp_model.n_jobs]['end_time'])
