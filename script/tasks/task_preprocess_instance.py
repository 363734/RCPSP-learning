import os
import sys
from typing import List

from script.Instances.RCPSPparser import parse_rcpsp, log_trivial_precedences, PSPLIB
from script.parameters import GENERATION_TIMES, DIR_DATAS, DIR_PREPROCESSED, DIR_SOLVER


def generate_all_for_one(bench: str, name: str, times: List[int]):
    data_file = os.path.join(DIR_DATAS, "{}/{}.sm".format(bench, name))
    triv_prec_file = os.path.join(DIR_PREPROCESSED, "{}/{}_trivial_prec.txt".format(bench, name))
    inst = parse_rcpsp(data_file, PSPLIB)
    log_trivial_precedences(inst, triv_prec_file)

    for sbps in ["true", "false"]:
        for vsids in ["true", "false"]:
            for time_out in times:
                opti_prec_file = os.path.join(DIR_PREPROCESSED,
                                              "{}/{}_all_prec_optimal_solution_TO={}_sbps={}_vsids={}.txt".format(
                                                  bench, name, time_out, sbps, vsids))
                print(opti_prec_file)
                out_file = os.path.join(DIR_PREPROCESSED, "{}/{}_run_TO={}_sbps={}_vsids={}.txt".format(
                    bench, name, time_out, sbps, vsids))
                print(out_file)
                os.system(
                    "{}/rcpsp-psplib {} ttef :print_prec_opti {} --sbps {} --vsids {} -t {} > {}".format(DIR_SOLVER,
                                                                                                        data_file,
                                                                                                        opti_prec_file,
                                                                                                        sbps, vsids,
                                                                                                        time_out,
                                                                                                        out_file))


if __name__ == "__main__":
    assert len(sys.argv) == 4
    bench = sys.argv[1]
    bench_group = int(sys.argv[2])
    instance_id = int(sys.argv[3])
    name = "{}{}_{}".format(bench, bench_group, instance_id)
    print(name)

    generate_all_for_one(bench, name, GENERATION_TIMES)
