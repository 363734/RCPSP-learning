import os
import sys

from script.Instances.benchPSPLIB import PSPLIB, read_arg_psplib
from script.logs import title_log, warning_log, step_log
from script.parameters import DIR_DATAS, DIR_DATA_PREPROCESSED, DIR_SOLVER


def generate(data_file: str, time_out: int, prefix_output_file: str, solver: str = 'chuffed'):
    if solver == 'chuffed':
        generate_chuffed(data_file, time_out, prefix_output_file)
    else:
        warning_log("Solver {} is not supported".format(formatting))
        exit(1)


def generate_chuffed(data_file: str, time_out: int, prefix_output_file: str):
    for sbps in ["true", "false"]:
        for vsids in ["true", "false"]:
            bsf_prec_file = os.path.join(DIR_DATA_PREPROCESSED,
                                         "{}_allprec_bsf_TO={}_sbps={}_vsids={}.txt".format(
                                             prefix_output_file, time_out, sbps, vsids))
            out_file = os.path.join(DIR_DATA_PREPROCESSED, "{}_run_TO={}_sbps={}_vsids={}.txt".format(
                prefix_output_file, time_out, sbps, vsids))
            step_log("Running chuffed with sbps={} and vsids={}".format(sbps, vsids))
            step_log("output file: {}".format(out_file))
            step_log("output prec file: {}".format(bsf_prec_file))
            os.system(
                "{}/rcpsp-psplib {} ttef :print_prec_opti {} --sbps {} --vsids {} -t {} > {}".format(DIR_SOLVER,
                                                                                                     data_file,
                                                                                                     bsf_prec_file,
                                                                                                     sbps, vsids,
                                                                                                     time_out,
                                                                                                     out_file))


if __name__ == "__main__":
    formatting = sys.argv[1]
    if formatting == PSPLIB:
        bench, bench_group, instance_id = read_arg_psplib(sys.argv, 2)
        name = "{}{}_{}".format(bench, bench_group, instance_id)
        solver = sys.argv[5]
        timeout = int(sys.argv[6])
        title_log("Solving file {} (psplib format) with {} under time out {}".format(name, solver, timeout))
        data_file = os.path.join(DIR_DATAS, "psplib/{}/{}.sm".format(bench, name))
        prefix_output_file = "psplib/{}/{}".format(bench, name)
    else:  # TODO add new format here
        warning_log("Format {} is not supported for the RCPSP instance".format(formatting))
        exit(1)

    generate(data_file, timeout, prefix_output_file, solver)
