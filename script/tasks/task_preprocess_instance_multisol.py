import math
import os
import sys

from script.Instances.benchPSPLIB import PSPLIB, read_arg_psplib
from script.logs import title_log, warning_log, step_log
from script.parameters import DIR_DATAS, DIR_DATA_PREPROCESSED, DIR_DATA_PREPROCESSED_MULTI, DIR_SOLVER


def generate_multi(data_file: str, time_out_ub:int, time_out: int, prefix_output_file: str, nb_sol:int, solver: str = 'chuffed'):
    if solver == 'chuffed':
        generate_chuffed_multi(data_file, time_out_ub, time_out, prefix_output_file, nb_sol)
    else:
        warning_log("Solver {} is not supported".format(formatting))
        exit(1)


def generate_chuffed_multi(data_file: str, time_out_ub:int, time_out: int, prefix_output_file: str, nb_sol:int):
    for sbps in ["true", "false"]:
        for vsids in ["true", "false"]:
            out_file_ub = os.path.join(DIR_DATA_PREPROCESSED, "{}_run_TO={}_sbps={}_vsids={}.txt".format(
                prefix_output_file, time_out_ub, sbps, vsids))
            ub = math.inf
            with open(out_file_ub) as file_ub:
                lines = file_ub.readlines()
                for k in range(len(lines)).__reversed__():
                    if lines[k][:10] == "makespan =":
                        ub = int(lines[k][10:])
                        break
            bsf_prec_file = os.path.join(DIR_DATA_PREPROCESSED_MULTI,
                                         "{}_allprec_bsf_ubto={}_TO={}_sbps={}_vsids={}.txt".format(
                                             prefix_output_file, time_out_ub, time_out, sbps, vsids))
            out_file = os.path.join(DIR_DATA_PREPROCESSED_MULTI, "{}_run_ubto={}_TO={}_sbps={}_vsids={}.txt".format(
                prefix_output_file, time_out_ub, time_out, sbps, vsids))
            step_log("Running chuffed with sbps={} and vsids={}".format(sbps, vsids))
            step_log("output file: {}".format(out_file))
            step_log("output prec file: {}".format(bsf_prec_file))
            os.system(
                "{}/rcpsp-psplib {} ttef :print_prec_opti {} :ub {} --sbps {} --vsids {} -t {} -n {} > {}".format(DIR_SOLVER,
                                                                                                     data_file,
                                                                                                     bsf_prec_file,
                                                                                                     ub,
                                                                                                     sbps, vsids,
                                                                                                     time_out, nb_sol,
                                                                                                     out_file))


if __name__ == "__main__":
    formatting = sys.argv[1]
    if formatting == PSPLIB:
        bench, bench_group, instance_id = read_arg_psplib(sys.argv, 2)
        name = "{}{}_{}".format(bench, bench_group, instance_id)
        solver = sys.argv[5]
        timeout_UB = int(sys.argv[6])
        timeout = int(sys.argv[7])
        nb_sol = int(sys.argv[8])
        title_log("Solving file {} (psplib format) with {} under time out {}, max {} solutions".format(name, solver, timeout, nb_sol))
        data_file = os.path.join(DIR_DATAS, "psplib/{}/{}.sm".format(bench, name))
        prefix_output_file = "psplib/{}/{}".format(bench, name)
    else:  # TODO add new format here
        warning_log("Format {} is not supported for the RCPSP instance".format(formatting))
        exit(1)

    generate_multi(data_file, timeout_UB, timeout, prefix_output_file, nb_sol, solver)
