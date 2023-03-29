import os
import sys

from script.Instances.RCPSPparser import parse_rcpsp

from script.PSPLIBinfo import BENCH, BENCH_GROUP

from script.parameters import PERCENTAGE_TRAINING, DIR_DATAS, DIR_PREPROCESSED, GENERATION_TIMES

from script.split_bench import split_bench, split_instance

if __name__ == "__main__":
    assert (len(sys.argv) == 2)
    tag = sys.argv[1]
    print("Creating bench tag={}".format(tag))
    split_bench(tag)

    for t in BENCH:
        for i in range(1, BENCH_GROUP[t]+1):
            for j in range(1, 11):
                name = "{}{}_{}".format(t, i, j)
                print("-" * 30)
                print("Generate bench split for instance {}".format(name))
                inst = parse_rcpsp(os.path.join(DIR_DATAS, "{}/{}.sm".format(t,name)))
                for perc in PERCENTAGE_TRAINING + ["0-100"]:
                    for to in GENERATION_TIMES:
                        for sbps in ['false', 'true']:
                            for vsids in ['false', 'true']:
                                sol_name = "{}/{}_all_prec_optimal_solution_TO={}_sbps={}_vsids={}.txt".format(
                                    t, name, to, sbps, vsids
                                )
                                print("Generate bench split for solution {}".format(sol_name))
                                split_instance(tag, perc, inst,
                                               os.path.join(DIR_PREPROCESSED, sol_name))
