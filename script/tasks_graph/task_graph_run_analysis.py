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
    formatting="psplib"
    output_dir = os.path.join(DIR_RESULTS_GRAPHS, "final_{}_{}".format(model, threshold))
    os.makedirs(output_dir, exist_ok=True)
    map_opt = {"true": "+sbps+vsids", "false": "no"}
    split = split_bench(formatting,split_tag)
    btch = Batch(split)
    # for opt in ["true"]:  # , "false"]:
    for opt in ["true", "false"]:
        for to in GENERATION_TIMES:
            # for to in [1000]:
            print("Generating graph for TO={}: reading results".format(to))
            results_init = parse_preprocessed_result(
                str(DIR_DATA_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
                "model", to)

            results_withprec = parse_result_final(
                str(DIR_RUN_RESULT) + "/" + model + "/run_addprec_{}_" + threshold + "_[" + model + "]_TO=" + str(
                    to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
                "model with prec", to)

            # results_withprec_firstsol = parse_result_final(
            #     str(DIR_RUN_RESULT) + "/" + model + "/runOne_addprec_{}_" + threshold + "_[" + model + "]_TO=60000_sbps=" + opt + "_vsids=" + opt + ".txt",
            #     "model with prec One", to)

            results_withorde = parse_result_final(
                str(DIR_RUN_RESULT) + "/" + model + "/run_ordering_{}_" + threshold + "_[" + model + "]_TO=" + str(
                    to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
                "model with orde", to)

            # results_withorde_firstsol = parse_result_final(
            #     str(DIR_RUN_RESULT) + "/" + model + "/runOne_ordering_{}_" + threshold + "_[" + model + "]_TO=60000_sbps=" + opt + "_vsids=" + opt + ".txt",
            #     "model with orde One", to)

            allgr={}
            for subgroup in ["seen", "unseen", "unknown", "all"]:
                grp = {}
                for b in PSPLIB_BENCH:
                    grp[b] = ["{}{}_{}".format(t, i, j) for t, i, j in btch.get_batch(subgroup, [b])]
                allgr[subgroup] = grp
            #
            #     print("Generating graph for TO={}: plotting graph".format(to))
            #     graph_best_so_far([results_init, results_withprec, results_withorde], grp,
            #                       # ,results_withprec_firstsol, results_withorde_firstsol],
            #                       "Best-so-far catus plot (group {}, TO={}, opt={}, model={})".format(subgroup.upper(), to, map_opt[opt], model),
            #                       os.path.join(output_dir,
            #                                    "final_result_cactus_bsf_{}_TO={}_opt={}_model=[{}]_threshold={}.pdf".format(
            #                                        subgroup.upper(), to,
            #                                        map_opt[
            #                                            opt],
            #                                        model,
            #                                        threshold)))
            #
            #     # graph_first_sol([results_init, results_withprec, results_withorde],
            #     #                 "First sol catus plot (group {}, TO={}, opt={}, model={})".format(subgroup.upper(), to, map_opt[opt], model),
            #     #                 os.path.join(output_dir,
            #     #                              "final_result_cactus_firstsol_{}_TO={}_opt={}_model=[{}]_threshold={}.pdf".format(
            #     #                                  subgroup,to,
            #     #                                  map_opt[
            #     #                                      opt],
            #     #                                  model,
            #     #                                  threshold)))
            #
            #     graph_time([results_init, results_withprec, results_withorde], grp,
            #                # ,results_withprec_firstsol, results_withorde_firstsol],
            #                "Time catus plot (group {}, TO={}, opt={}, model={})".format(subgroup.upper(), to, map_opt[opt], model),
            #                os.path.join(output_dir,
            #                             "final_result_cactus_time_{}_TO={}_opt={}_model=[{}]_threshold={}.pdf".format(subgroup.upper(), to,
            #                                                                                                        map_opt[
            #                                                                                                            opt],
            #                                                                                                        model,
            # threshold)))
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
            graph_time_grouped([results_init, results_withprec, results_withorde], allgr,
                                      # ,results_withprec_firstsol, results_withorde_firstsol],
                                      "Time catus plot catus plot (TO={}, opt={}, model={})".format(to, map_opt[opt],
                                                                                                model),
                                      os.path.join(output_dir,
                                                   "final_result_cactus_time_TO={}_opt={}_model=[{}]_threshold={}.pdf".format(
                                                       to,
                                                       map_opt[
                                                           opt],
                                                       model,
                                                       threshold)))
