import math
import os
import sys

from script.PSPLIBinfo import from_bench

from script.Instances.upperbound import load_bounds

from script.graphs.result_run_solver import parse_preprocessed_result, parse_result_final
from script.parameters import DIR_PREPROCESSED, GENERATION_TIMES, DIR_RESULTS_GRAPHS, DIR_RUN_RESULT


def compare(baseline, other):
    cnt = {"best": 0, "equal": 0, "worse": 0, "total": 0, "nosol":0,"missing":[], "bestrec":[]}
    for key in baseline:
        if from_bench(key) == "j120":
            if key in other:
                if other[key]['best'] != math.inf:
                    cnt['total'] += 1
                    if baseline[key]['ub'] > other[key]['best']:
                        cnt['best'] += 1
                        cnt["bestrec"].append((key,other[key]['best'], baseline[key]['ub']))
                    elif baseline[key]['ub'] == other[key]['best']:
                        cnt['equal'] += 1
                    else:
                        cnt['worse'] += 1
                else:
                    cnt["nosol"] += 1
            else:
                cnt["missing"].append(key)
    return cnt

def compare_bis(baseline, other):
    cnt = {"best": 0, "equal": 0, "worse": 0, "total": 0, "nosol":0,"missing":[], "bestrec":[]}
    for key in baseline:
        if from_bench(key) == "j120":
            if key in other:
                if other[key]['best'] != math.inf:
                    cnt['total'] += 1
                    if baseline[key]['best'] > other[key]['best']:
                        cnt['best'] += 1
                        cnt["bestrec"].append((key,other[key]['best'], baseline[key]['best']))
                    elif baseline[key]['best'] == other[key]['best']:
                        cnt['equal'] += 1
                    else:
                        cnt['worse'] += 1
                else:
                    cnt["nosol"] += 1
            else:
                cnt["missing"].append(key)
    return cnt
def ratio_obj(baseline, other):
    r = []
    for key in baseline:
        if from_bench(key) == "j120":
            if other[key]["best"] != math.inf:
                r.append(other[key]["best"]/baseline[key]["best"])
    return r
def count_time(line):
    cnt = {"to":0,"noto":0}
    for key in line:
        if from_bench(key) == "j120":
            if line[key]["time"] == -1:
                cnt['to']+=1
            else:
                cnt['noto'] +=1
    return cnt
def ratio(baseline, other):
    r = []
    for key in baseline:
        if from_bench(key) == "j120":
            r.append(other[key]["time"]/baseline[key]["time"])
    return r


if __name__ == "__main__":
    model = sys.argv[1]
    threshold = sys.argv[2]
    split_tag = sys.argv[3]

    dir = os.path.join(DIR_RESULTS_GRAPHS, "analysis_res_stats")
    os.makedirs(dir, exist_ok=True)
    with open(os.path.join(dir,"stats.txt"), "w") as file:
        best_dict = load_bounds(os.path.join(DIR_PREPROCESSED, "bounds.txt"))

        res = {}

        for opt in ["true", "false"]:
            for to in GENERATION_TIMES:
                file.write("=" * 30+"\n")
                file.write("Stats for TO={} and opt={}\n".format(to, opt))
                file.write("=" * 30+"\n")

                results_init = parse_preprocessed_result(
                    str(DIR_PREPROCESSED) + "/{}/{}_run_TO=" + str(to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
                    "model", to).dict

                results_withprec = parse_result_final(
                    str(DIR_RUN_RESULT) + "/" + model + "/run_addprec_{}_" + threshold + "_[" + model + "]_TO=" + str(
                        to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
                    "model with prec", to).dict

                results_withorde = parse_result_final(
                    str(DIR_RUN_RESULT) + "/" + model + "/run_ordering_{}_" + threshold + "_[" + model + "]_TO=" + str(
                        to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
                    "model with orde", to).dict

                file.write("compare best to with init:\n")
                file.write(str(compare(best_dict, results_init)) + "\n")
                file.write(str(count_time(results_init))+"\n")

                file.write("compare best to with prec:\n")
                file.write(str(compare(best_dict, results_withprec))+"\n")
                file.write(str(compare_bis(results_init, results_withprec))+"\n")
                # rat = ratio_obj(results_init, results_withprec)
                # print(rat)
                # file.write("ratio best mean {}, min {}, max {}\n".format(sum(rat)/len(rat), min(rat), max(rat)))
                # rat = ratio(results_init, results_withprec)
                # file.write(str(count_time(results_withprec))+"\n")
                # file.write("ratio time mean {}, min {}, max {}\n".format(sum(rat)/len(rat), min(rat), max(rat)))

                file.write("compare best to with orde:\n")
                file.write(str(compare(best_dict, results_withorde))+"\n")
                file.write(str(compare_bis(results_init, results_withorde))+"\n")
                # rat = ratio_obj(results_init, results_withprec)
                # file.write("ratio best mean {}, min {}, max {}\n".format(sum(rat)/len(rat), min(rat), max(rat)))
                # rat = ratio(results_init, results_withorde)
                # file.write(str(count_time(results_withorde))+"\n")
                # file.write("ratio time mean {}, min {}, max {}\n".format(sum(rat)/len(rat), min(rat), max(rat)))
