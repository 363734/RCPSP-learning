import os
from typing import List

from script.parameters import DIR_TARGET, DIR_PREPROCESSED, DIR_RESULTS_GRAPHS

from script.Instances.upperbound import load_bounds
from script.PSPLIBinfo import BENCH, BENCH_GROUP
from script.graphs.result_run_solver import ResultRunSolver


def crop(c, time_out):
    x_bis = [i for i in c[0] if i <= time_out / 1000]
    y_bis = c[1][:len(x_bis)]
    return x_bis, y_bis


def graph_time(bench: List[ResultRunSolver], title: str, outputfile):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, sharex='col', sharey="row")
    fig.suptitle(title)
    fig.set_figwidth(10)
    fig.set_figheight(10)
    axslist = [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]]
    for ax in axslist:
        ax.set_xscale('log')
    axslist[0].set_ylabel("% of instances")
    axslist[2].set_xlabel("time (sec)")
    axslist[2].set_ylabel("% of instances")
    axslist[3].set_xlabel("time (sec)")
    to = max([b.time_out for b in bench]) / 1000
    for b in bench:
        d = b.cactus_line_by_bench_time()
        for i in range(len(BENCH)):
            t = BENCH[i]
            x, y = crop(d[t], b.time_out)
            axslist[i].plot(x, y, label=b.name)
    for i in range(len(BENCH)):
        t = BENCH[i]
        axslist[i].set_title(t)
        axslist[i].grid()
        axslist[i].legend()
        axslist[i].set_xlim([0, to])
        axslist[i].set_ylim([0, 1])

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputfile)


def graph_best_so_far(bench: List[ResultRunSolver], title: str, outputfile):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, sharex='col', sharey="row")
    fig.suptitle(title)
    fig.set_figwidth(10)
    fig.set_figheight(10)
    axslist = [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]]
    for ax in axslist:
        ax.set_xscale('log')
    axslist[0].set_ylabel("% of instances")
    axslist[2].set_xlabel("obj")
    axslist[2].set_ylabel("% of instances")
    axslist[3].set_xlabel("obj")
    # to = max([b.time_out for b in bench]) / 1000
    best_dict = load_bounds(os.path.join(DIR_PREPROCESSED, "bounds.txt"))
    for i in range(len(BENCH)):
        t = BENCH[i]
        x = [0] + [t for t in [best_dict[k]['ub'] for k in best_dict if k.startswith(t)] if t >= 0]
        x.sort()
        y = [j / (BENCH_GROUP[t] * 10) for j in list(range(len(x)))]
        axslist[i].plot(x, y, label="UB")
    for b in bench:
        d = b.cactus_line_by_bench_best()
        print(b.name)
        print(d)
        for i in range(len(BENCH)):
            t = BENCH[i]
            x, y = d[t]
            axslist[i].plot(x, y, label=b.name)
    for i in range(len(BENCH)):
        t = BENCH[i]
        axslist[i].set_title(t)
        axslist[i].grid()
        axslist[i].legend()
        # axslist[i].set_xlim([0, to])
        axslist[i].set_ylim([0, 1])

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputfile)

def graph_first_sol(bench: List[ResultRunSolver], title: str, outputfile):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, sharex='col', sharey="row")
    fig.suptitle(title)
    fig.set_figwidth(10)
    fig.set_figheight(10)
    axslist = [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]]
    for ax in axslist:
        ax.set_xscale('log')
    axslist[0].set_ylabel("% of instances")
    axslist[2].set_xlabel("obj")
    axslist[2].set_ylabel("% of instances")
    axslist[3].set_xlabel("obj")
    # to = max([b.time_out for b in bench]) / 1000
    best_dict = load_bounds(os.path.join(DIR_PREPROCESSED, "bounds.txt"))
    for i in range(len(BENCH)):
        t = BENCH[i]
        x = [0] + [t for t in [best_dict[k]['ub'] for k in best_dict if k.startswith(t)] if t >= 0]
        x.sort()
        y = [j / (BENCH_GROUP[t] * 10) for j in list(range(len(x)))]
        axslist[i].plot(x, y, label="UB")
    for b in bench:
        d = b.cactus_line_by_bench_first()
        for i in range(len(BENCH)):
            t = BENCH[i]
            x, y = d[t]
            axslist[i].plot(x, y, label=b.name)
    for i in range(len(BENCH)):
        t = BENCH[i]
        axslist[i].set_title(t)
        axslist[i].grid()
        axslist[i].legend()
        # axslist[i].set_xlim([0, to])
        axslist[i].set_ylim([0, 1])

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputfile)

if __name__ == "__main__":
    print("hello")
    results_to1s = ResultRunSolver(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=1000_sbps=OFF.txt", "TO=1s", 1000)
    results_to1m = ResultRunSolver(str(DIR_PREPROCESSED) + "/{}/{}_run_TO=60000_sbps=OFF.txt", "TO=1m", 60000)

    graph_best_so_far([results_to1s, results_to1m], "testtitle",os.path.join(DIR_RESULTS_GRAPHS, "g.pdf"))
    graph_time([results_to1s, results_to1m], "testtitle",os.path.join(DIR_RESULTS_GRAPHS, "g_time.pdf"))
