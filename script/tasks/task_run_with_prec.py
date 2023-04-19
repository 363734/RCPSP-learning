import os
import sys
from typing import List

#from script.Instances.RCPSPparser import parse_rcpsp, PSPLIB
from script.parameters import GENERATION_TIMES, DIR_DATAS, DIR_SOLVER, DIR_PREDICTIONS, DIR_RUN_RESULT


def generate_all_for_one(bench: str, name: str, times: List[int], model: str, threshold: float):
    data_file = os.path.join(DIR_DATAS, "{}/{}.sm".format(bench, name))
    train_prec = os.path.join(DIR_PREDICTIONS, model, "prec_{}_{}_[{}].txt".format(name, threshold, model))
    train_orde = os.path.join(DIR_PREDICTIONS, model, "orde_{}_{}_[{}].txt".format(name, threshold, model))
    #inst = parse_rcpsp(data_file, PSPLIB)

    for opt in ["true", "false"]:
        out_file_ordering_1 = os.path.join(DIR_RUN_RESULT, model,
                                           "runOne_ordering_{}_{}_[{}]_TO={}_sbps={}_vsids={}.txt".format(
                                               name, threshold, model, 60000, opt, opt))
        os.system(
            '{}/rcpsp-psplib {} ttef :add_ordering "{}" --sbps {} --vsids {} -t {} -n 1 > "{}"'.format(DIR_SOLVER,
                                                                                                      data_file,
                                                                                                      train_orde,
                                                                                                      opt, opt,
                                                                                                      60000,
                                                                                                      out_file_ordering_1))

        out_file_addprec_1 = os.path.join(DIR_RUN_RESULT, model,
                                        "runOne_addprec_{}_{}_[{}]_TO={}_sbps={}_vsids={}.txt".format(
                                            name, threshold, model, 60000, opt, opt))

        os.system(
            '{}/rcpsp-psplib {} ttef :add_prec "{}" --sbps {} --vsids {} -t {} -n 1 > "{}"'.format(DIR_SOLVER,
                                                                                              data_file,
                                                                                              train_prec,
                                                                                              opt, opt,
                                                                                              60000,
                                                                                              out_file_addprec_1))
        for time_out in times:
            print("TO={} opt={}".format(time_out,opt))
            out_file_ordering = os.path.join(DIR_RUN_RESULT, model,
                                             "run_ordering_{}_{}_[{}]_TO={}_sbps={}_vsids={}.txt".format(
                                                 name, threshold, model, time_out, opt, opt))
            os.system(
                '{}/rcpsp-psplib {} ttef :add_ordering "{}" --sbps {} --vsids {} -t {} > "{}"'.format(DIR_SOLVER,
                                                                                              data_file,
                                                                                              train_orde,
                                                                                              opt, opt,
                                                                                              time_out,
                                                                                              out_file_ordering))


            out_file_addprec = os.path.join(DIR_RUN_RESULT, model,
                                            "run_addprec_{}_{}_[{}]_TO={}_sbps={}_vsids={}.txt".format(
                                                name, threshold, model, time_out, opt, opt))

            os.system(
                '{}/rcpsp-psplib {} ttef :add_prec "{}" --sbps {} --vsids {} -t {} > "{}"'.format(DIR_SOLVER,
                                                                                              data_file,
                                                                                              train_prec,
                                                                                              opt, opt,
                                                                                              time_out,
                                                                                              out_file_addprec))


if __name__ == "__main__":
    assert len(sys.argv) == 6
    bench = sys.argv[1]
    bench_group = int(sys.argv[2])
    instance_id = int(sys.argv[3])
    model = sys.argv[4]
    threshold = float(sys.argv[5])
    name = "{}{}_{}".format(bench, bench_group, instance_id)
    print(name)

    generate_all_for_one(bench, name, GENERATION_TIMES, model, threshold)