import os

from script.graphs.dataset import graph_best_so_far, graph_time

from script.graphs.result_run_solver import parse_preprocessed_result
from script.parameters import DIR_PREPROCESSED, GENERATION_TIMES, DIR_RESULTS_GRAPHS

if __name__ == "__main__":

    for to in GENERATION_TIMES:
        print("Generating graph for TO={}: reading results".format(to))
        results_noopt = parse_preprocessed_result(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=false_vsids=false.txt",
                                        "model", to)
        results_sbps = parse_preprocessed_result(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=true_vsids=false.txt",
                                       "model+sbps", to)
        results_vsids = parse_preprocessed_result(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=false_vsids=true.txt",
                                        "model+vsids", to)
        results_sbpsvsids = parse_preprocessed_result(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=true_vsids=true.txt",
                                            "model+sbps+vsids", to)
        print("Generating graph for TO={}: plotting graph".format(to))
        graph_best_so_far([results_noopt, results_sbps, results_vsids, results_sbpsvsids],
                          "Best-so-far catus plot (TO={})".format(to),
                          os.path.join(DIR_RESULTS_GRAPHS, "cactus_bsf_TO={}.pdf".format(to)))

        graph_time([results_noopt, results_sbps, results_vsids, results_sbpsvsids],
                          "Time catus plot (TO={})".format(to),
                          os.path.join(DIR_RESULTS_GRAPHS, "cactus_time_TO={}.pdf".format(to)))
