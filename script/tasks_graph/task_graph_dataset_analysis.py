import os

from script.graphs.dataset import graph_best_so_far, graph_time

from script.graphs.result_run_solver import ResultRunSolver
from script.parameters import DIR_PREPROCESSED, GENERATION_TIMES, DIR_RESULTS_GRAPHS

if __name__ == "__main__":

    for to in GENERATION_TIMES:
        results_noopt = ResultRunSolver(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=false_vsids=false.txt",
                                        "model", to)
        results_sbps = ResultRunSolver(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=true_vsids=false.txt",
                                       "model+sbps", to)
        results_vsids = ResultRunSolver(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=false_vsids=true.txt",
                                        "model+vsids", to)
        results_sbpsvsids = ResultRunSolver(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=true_vsids=true.txt",
                                            "model+sbps+vsids", to)

        graph_best_so_far([results_noopt, results_sbps, results_vsids, results_sbpsvsids],
                          "Best-so-far catus plot (TO={})".format(to),
                          os.path.join(DIR_RESULTS_GRAPHS, "cactus_bsf_TO={}.pdf".format(to)))

        graph_time([results_noopt, results_sbps, results_vsids, results_sbpsvsids],
                          "Time catus plot (TO={})".format(to),
                          os.path.join(DIR_RESULTS_GRAPHS, "cactus_bsf_TO={}.pdf".format(to)))
