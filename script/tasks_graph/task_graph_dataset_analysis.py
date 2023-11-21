import os

from script.graphs.dataset import graph_best_so_far, graph_time, graph_time_init, graph_best_so_far_init

from script.graphs.result_run_solver import parse_preprocessed_result
from script.parameters import DIR_DATA_PREPROCESSED, GENERATION_TIMES, DIR_RESULTS_GRAPHS

if __name__ == "__main__":

    res = {}

    for to in GENERATION_TIMES:
        res[to] = {}
        print("Generating graph for TO={}: reading results".format(to))
        res[to]["nopt"] = parse_preprocessed_result(
            str(DIR_DATA_PREPROCESSED) + "/psplib/{}/{}_run_TO=" + str(to) + "_sbps=false_vsids=false.txt",
            "model", to)
        res[to]["sbps"] = parse_preprocessed_result(
            str(DIR_DATA_PREPROCESSED) + "/psplib/{}/{}_run_TO=" + str(to) + "_sbps=true_vsids=false.txt",
            "model+sbps", to)
        res[to]["vsids"] = parse_preprocessed_result(
            str(DIR_DATA_PREPROCESSED) + "/psplib/{}/{}_run_TO=" + str(to) + "_sbps=false_vsids=true.txt",
            "model+vsids", to)
        res[to]["sbps+vsids"] = parse_preprocessed_result(
            str(DIR_DATA_PREPROCESSED) + "/psplib/{}/{}_run_TO=" + str(to) + "_sbps=true_vsids=true.txt",
            "model+sbps+vsids", to)


    dir = os.path.join(DIR_RESULTS_GRAPHS, "analysis_dataset")
    os.makedirs(dir, exist_ok=True)
    graph_best_so_far_init(res, "Best-so-far catus plot", os.path.join(dir, "cactus_bsf.pdf"))

    graph_time_init(res, "Time catus plot", os.path.join(dir, "cactus_time.pdf"))
