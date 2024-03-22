import os
from typing import List

from script.Instances.benchPSPLIB import PSPLIB, from_bench, PSPLIB_BENCH
from script.Instances.upperbound import load_bounds
from script.graphs.result_run_solver import ResultRunSolver, parse_result_greedy, parse_result_final
from script.parameters import DIR_DATAS, DIR_DATA_PREPROCESSED, DIR_RUN_RESULT_GREEDY, DIR_RUN_RESULT
from script.save_pickle_json import j_load


def get_sirene_result():
    sirene_results_file = os.path.join(DIR_DATAS, PSPLIB, "sirene", "inference-sgs_vs_cpsat.json")
    sirene_dataset_file = os.path.join(DIR_DATAS, PSPLIB, "sirene", "bench_list_postpro_merged.json")
    sirene_results = j_load(sirene_results_file)
    sirene_dataset = j_load(sirene_dataset_file)

    # best_dict = load_bounds(os.path.join(DIR_DATA_PREPROCESSED,"psplib", "bounds.txt"))
    d = {}
    for key in sirene_results:
        e = sirene_results[key]
        # print(e["benchmark_id"])
        # print(e["feasibility_abs_makespan"])
        # print(sirene_dataset[e["benchmark_id"]])
        # print(e["feasibility_abs_makespan"] >= best_dict[sirene_dataset[e["benchmark_id"]]]['ub'])
        d[sirene_dataset[e["benchmark_id"]]] = {'best': e["feasibility_abs_makespan"]}
    subset = {'j30': [], 'j60': [], 'j90': [], 'j120': []}
    for key in d:
        t = from_bench(key)
        subset[t] += [key]
    return ResultRunSolver('Sirene', None, d), subset


def graph_compare_to_sirene(bench: List[ResultRunSolver], grp, outputfile):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter
    fig, axs = plt.subplots(1, 4, sharex='col', sharey="row")
    # fig.suptitle(title)
    fig.set_figwidth(10)
    fig.set_figheight(7)
    for j in range(4):
        axs[j].set_xscale('log')
    axs[0].set_ylabel("% of instances")
    for j in range(4):
        axs[j].set_title(PSPLIB_BENCH[j].upper())
        axs[j].set_xlabel("obj")
        axs[j].xaxis.set_major_formatter(ScalarFormatter())
    best_dict = load_bounds(os.path.join(DIR_DATA_PREPROCESSED,"psplib", "bounds.txt"))
    for j in range(len(PSPLIB_BENCH)):
        t = PSPLIB_BENCH[j]
        x = [0] + [p for p in [best_dict[k]['ub'] for k in grp[t]] if p >= 0]
        x.sort()
        y = [p / len(grp[t]) for p in list(range(len(x)))]
        axs[j].plot(x, y, 'k', label="UB", linewidth=1)
    for b in bench:
        d = b.cactus_line_by_bench_best(grp)
        for k in range(len(PSPLIB_BENCH)):
            t = PSPLIB_BENCH[k]
            x, y = d[t]
            axs[k].plot(x, y, label=b.name, linewidth=1)
    for j in range(len(PSPLIB_BENCH)):
        axs[j].grid()
        # axs[i, j].legend()
        axs[j].set_ylim([0, 1])
    axs[0].set_xticks([30, 40, 50, 60, 100, 200])
    axs[1].set_xticks([60, 100])
    axs[2].set_xticks([60, 100, 200, 300])
    axs[3].set_xticks([100, 200, 300, 500])

    axs[0].legend(loc='lower left')

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(outputfile, bbox_inches='tight')

def graph_compare_to_sirene_sgs_j120(bench: List[ResultRunSolver], grp, outputfile):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter
    fig, axs = plt.subplots(1, 1, sharex='col', sharey="row")
    # fig.suptitle(title)
    fig.set_figwidth(4)
    fig.set_figheight(2.5)
    axs.set_xscale('log')
    axs.set_ylabel("% of instances")
    axs.set_title("Subset of J120 (112 instances)")
    axs.set_xlabel("obj")
    axs.xaxis.set_major_formatter(ScalarFormatter())
    best_dict = load_bounds(os.path.join(DIR_DATA_PREPROCESSED,"psplib", "bounds.txt"))

    t = 'j120'
    x = [0] + [p for p in [best_dict[k]['ub'] for k in grp[t]] if p >= 0]
    x.sort()
    y = [p / len(grp[t]) for p in list(range(len(x)))]
    axs.plot(x, y, 'k', label="UB", linewidth=1)

    for b in bench:
        d = b.cactus_line_by_bench_best(grp)
        x, y = d[t]
        axs.plot(x, y, label=b.name, linewidth=1)

    print(len(grp[t]))
    axs.grid()
    # axs[i, j].legend()
    axs.set_ylim([0, 1])
    axs.set_xticks([100, 200, 300, 400, 500])

    axs.legend(loc='lower right',prop = { "size": 8 })

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(outputfile, bbox_inches='tight')

def graph_compare_to_sirene_j120(bench: List[ResultRunSolver], grp, outputfile):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter
    fig, axs = plt.subplots(1, 1, sharex='col', sharey="row")
    # fig.suptitle(title)
    fig.set_figwidth(3.5)
    fig.set_figheight(2)
    axs.set_xscale('log')
    axs.set_ylabel("% of instances")
    axs.set_title("Subset of J120 (112 instances)")
    axs.set_xlabel("obj")
    axs.xaxis.set_major_formatter(ScalarFormatter())
    best_dict = load_bounds(os.path.join(DIR_DATA_PREPROCESSED, "psplib", "bounds.txt"))

    t = 'j120'
    x = [0] + [p for p in [best_dict[k]['ub'] for k in grp[t]] if p >= 0]
    x.sort()
    y = [p / len(grp[t]) for p in list(range(len(x)))]
    axs.plot(x, y, 'k', label="UB", linewidth=1)

    for b in bench:
        d = b.cactus_line_by_bench_best(grp)
        x, y = d[t]
        axs.plot(x, y, label=b.name, linewidth=1)

    print(len(grp[t]))
    axs.grid()
    # axs[i, j].legend()
    axs.set_ylim([0, 1])
    axs.set_xlim([0, 350])
    axs.set_xticks([100, 200, 300])

    axs.legend(loc='lower right',prop = { "size": 8 })

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(outputfile, bbox_inches='tight')

sirene_res , gr = get_sirene_result()
model = "sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=true_vsids=true]_0.01_bsfLoss"
thresholds = [0.5, 0.55, 0.75, 0.95, 0.99]
result_greedyB = [parse_result_greedy(
        str(DIR_RUN_RESULT_GREEDY) + "/" + model + "/t" + str(threshold) + "/run_greedy_{}_" + str(threshold) + "_[" + model + "].txt",
        "orde + SGS {}".format(threshold)) for threshold in thresholds]
model = "sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=false_vsids=false]_0.01_bsfLoss"
thresholds = [0.5, 0.55, 0.75, 0.95, 0.99]
result_greedyA = [parse_result_greedy(
        str(DIR_RUN_RESULT_GREEDY) + "/" + model + "/t" + str(threshold) + "/run_greedy_{}_" + str(threshold) + "_[" + model + "].txt",
        "orde + SGS {}".format(threshold)) for threshold in thresholds]
graph_compare_to_sirene([sirene_res]+result_greedyA+result_greedyB, gr, "sgrALL.pdf")
graph_compare_to_sirene_sgs_j120([sirene_res] + result_greedyB, gr, "sgrJ120.pdf")

model = "sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=true_vsids=true]_0.01_bsfLoss"
threshold = str(0.50)
opt="true"
to=3600000
resultModBorde=parse_result_final(
                str(DIR_RUN_RESULT) + "/" + model + "/run_ordering_{}_" + threshold + "_[" + model + "]_TO=" + str(
                    to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
                "model B with orde 0.50", to)
threshold= str(0.99)
resultModBprec=parse_result_final(
                str(DIR_RUN_RESULT) + "/" + model + "/run_addprec_{}_" + threshold + "_[" + model + "]_TO=" + str(
                    to) + "_sbps=" + opt + "_vsids=" + opt + ".txt",
                "model B with prec 0.99", to)

graph_compare_to_sirene_j120([sirene_res, resultModBorde, resultModBprec], gr, "sireneJ120.pdf")
