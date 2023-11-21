import os
import sys

from script.Instances.bench import mapfctformat
# from script.Instances.bench import mapfctformat

from script.logs import title_log
from script.parameters import DIR_SPLIT

from script.split_bench import split_bench

if __name__ == "__main__":
    formatting = sys.argv[1]
    tag = sys.argv[2]
    if len(sys.argv) == 3:
        split_bench(formatting, tag)
    elif len(sys.argv) > 3:
        u_or_b = sys.argv[3] # uniform or balanced
        precfileopt = sys.argv[4]
        title_log("Creating split tag={} for bench {} with options [{}]".format(tag, formatting, precfileopt))
        dir_name = os.path.join(DIR_SPLIT, formatting, tag)
        os.makedirs(dir_name, exist_ok=True)
        mapfctformat[formatting]["split_instances_cross"](tag, precfileopt, u_or_b)
        # if formatting == PSPLIB:
        #     for t in PSPLIB_BENCH:
        #         for i in range(1, PSPLIB_BENCH_GROUP[t] + 1):
        #             for j in range(1, 11):
        #                 name = "{}{}_{}".format(t, i, j)
        #                 step_log("Generate bench split for instance {}".format(name))
        #                 inst = parse_rcpsp(os.path.join(DIR_DATAS, "psplib/{}/{}.sm".format(t, name)))
        #                 sol_name = "{}/{}_{}.txt".format(t, name, precfileopt)
        #                 print("Generate bench split for solution {}".format(sol_name))
        #                 split_instance_cross(tag, inst, os.path.join(DIR_DATA_PREPROCESSED, sol_name))
        # else:  # TODO add new format here
        #     warning_log("Format {} is not supported for the RCPSP instance".format(formatting))
        #     exit(1)
