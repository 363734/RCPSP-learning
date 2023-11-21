import os
import sys

from script.Instances.benchPSPLIB import PSPLIB_BENCH

from script.GNN.dglBatch import Batch

from script.split_bench import split_bench

from script.graphs.dataset import graph_best_so_far, graph_time, graph_best_so_far_grouped, graph_time_grouped

from script.graphs.result_run_solver import ResultRunSolver, parse_preprocessed_result, parse_result_final
from script.parameters import DIR_DATA_PREPROCESSED, GENERATION_TIMES, DIR_RESULTS_GRAPHS, DIR_RUN_RESULT

if __name__ == "__main__":
    model = sys.argv[1]
    threshold = sys.argv[2]
    split_tag = sys.argv[3]
    output_dir = os.path.join(DIR_RESULTS_GRAPHS, "final_{}_{}".format(model, threshold))
    os.makedirs(output_dir, exist_ok=True)
    map_opt = {"true": "+sbps+vsids", "false": "no"}
    split = split_bench(split_tag)
    btch = Batch(split)
    # for opt in ["true"]:  # , "false"]:
    opt = "true"
    to = 3600000
    # for to in [1000]:
    print("Generating graph for TO={}: reading results".format(to))
    results_init = parse_preprocessed_result(
        str(DIR_DATA_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
        "model", to)

    results_withprec = parse_result_final(
        str(DIR_RUN_RESULT) + "/" + model + "/run_addprec_{}_" + threshold + "_[" + model + "]_TO=" + str(
            to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
        "model with prec", to)

    results_withorde = parse_result_final(
        str(DIR_RUN_RESULT) + "/" + model + "/run_ordering_{}_" + threshold + "_[" + model + "]_TO=" + str(
            to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
        "model with orde", to)


    allgr={}
    for subgroup in ["seen", "unseen", "unknown", "all"]:
        grp = {}
        for b in PSPLIB_BENCH:
            grp[b] = ["{}{}_{}".format(t, i, j) for t, i, j in btch.get_batch(subgroup, [b])]
        allgr[subgroup] = grp

    graph_best_so_far_grouped([results_init, results_withprec, results_withorde], allgr,
                          # ,results_withprec_firstsol, results_withorde_firstsol],
                          "Best-so-far catus plot (TO={}, opt={}, model={})".format(to, map_opt[opt],
                                                                                    model),
                          os.path.join(output_dir,
                                       "final_result_cactus_bsf_TO={}_opt={}_model=[{}]_threshold={}.pdf".format(
                                           to,
                                           map_opt[
                                               opt],
                                           model,
                                           threshold)))
