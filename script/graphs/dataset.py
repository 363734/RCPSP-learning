import os
from typing import List

from script.parameters import DIR_TARGET, DIR_DATA_PREPROCESSED, DIR_RESULTS_GRAPHS, GENERATION_TIMES

from script.Instances.upperbound import load_bounds
from script.Instances.benchPSPLIB import PSPLIB_BENCH, PSPLIB_BENCH_GROUP
from script.graphs.result_run_solver import ResultRunSolver
from script.split_bench import SUBSPLIT


def crop(c, time_out):
    x_bis = [i for i in c[0] if i <= time_out / 1000]
    y_bis = c[1][:len(x_bis)]
    return x_bis, y_bis


def graph_time(bench: List[ResultRunSolver], grp, title: str, outputfile):
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
        d = b.cactus_line_by_bench_time(grp)
        for i in range(len(PSPLIB_BENCH)):
            t = PSPLIB_BENCH[i]
            x, y = crop(d[t], b.time_out)
            axslist[i].plot(x, y, label=b.name)
    for i in range(len(PSPLIB_BENCH)):
        t = PSPLIB_BENCH[i]
        axslist[i].set_title(t)
        axslist[i].grid()
        axslist[i].legend()
        axslist[i].set_xlim([0, to])
        axslist[i].set_ylim([0, 1])

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputfile, bbox_inches='tight')


def graph_time_init(data, title: str, outputfile):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(len(data), len(PSPLIB_BENCH), sharey="row")
    # fig.suptitle(title)
    fig.set_figwidth(10)
    fig.set_figheight(6)
    for i in range(len(GENERATION_TIMES)):
        for b in data[GENERATION_TIMES[i]]:
            d = data[GENERATION_TIMES[i]][b].cactus_line_by_bench_time_all()
            for k in range(len(PSPLIB_BENCH)):
                t = PSPLIB_BENCH[k]
                x, y = crop(d[t], data[GENERATION_TIMES[i]][b].time_out)
                axs[i, k].plot(x, y, label=data[GENERATION_TIMES[i]][b].name, linewidth=1)
                axs[i, k].set_xlim(left=0.01005)
        axs[i, 0].set_ylabel("TO={}sec\n% of instances".format(int(GENERATION_TIMES[i]/1000)), multialignment='center')
        axs[i, 0].set_ylim([0, 1])

    for j in range(len(PSPLIB_BENCH)):
        t = PSPLIB_BENCH[j]
        axs[0, j].set_title(t.upper())
        axs[len(data) - 1, j].set_xlabel("time (sec)")
    for i in range(len(GENERATION_TIMES)):
        for j in range(len(PSPLIB_BENCH)):
            axs[i, j].set_xscale('log')
            axs[i, j].set_xlim([0, GENERATION_TIMES[i] / 1000])
            axs[i, j].grid()
            # axs[i,j].xaxis.set_tick_params(fontsize=7)
            # axs[i, j].legend()
    axs[len(GENERATION_TIMES)-1,0].legend(loc='lower left')
    # plt.xticks(fontsize=12)#, rotation=90)
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(wspace=0, hspace=0.25)
    plt.savefig(outputfile, bbox_inches='tight')


def graph_time_grouped(bench: List[ResultRunSolver], grp, title: str, outputfile):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(4, 4, sharex='col', sharey="row")
    # fig.suptitle(title)
    fig.set_figwidth(10)
    fig.set_figheight(7)
    for i in range(4):
        for j in range(4):
            axs[i, j].set_xscale('log')
            # axs[i, j].set_ylabel("{} - % of instances".format(SUBSPLIT[i].upper()))
        axs[i, 0].set_ylabel("{}\n% of instances".format(SUBSPLIT[i].upper()))
    for j in range(4):
        axs[0, j].set_title(PSPLIB_BENCH[j].upper())
        axs[3, j].set_xlabel("time (sec)")
    for i in range(len(SUBSPLIT)):
        s = SUBSPLIT[i]
        for b in bench:
            d = b.cactus_line_by_bench_time(grp[s])
            for k in range(len(PSPLIB_BENCH)):
                t = PSPLIB_BENCH[k]
                x, y = d[t]
                axs[i, k].plot(x, y, label=b.name, linewidth=1)

        for j in range(len(PSPLIB_BENCH)):
            axs[i, j].grid()
            # axs[i, j].legend()
            axs[i, j].set_ylim([0, 1])
    axs[len(GENERATION_TIMES)-1,0].legend(loc='lower left')

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(outputfile, bbox_inches='tight')


def graph_best_so_far(bench: List[ResultRunSolver], grp, title: str, outputfile):
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
    best_dict = load_bounds(os.path.join(DIR_DATA_PREPROCESSED, "bounds.txt"))
    for i in range(len(PSPLIB_BENCH)):
        t = PSPLIB_BENCH[i]
        x = [0] + [p for p in [best_dict[k]['ub'] for k in grp[t]] if p >= 0]
        x.sort()
        y = [j / len(grp[t]) for j in list(range(len(x)))]
        axslist[i].plot(x, y, label="UB")
    for b in bench:
        d = b.cactus_line_by_bench_best(grp)
        print(b.name)
        print(d)
        for i in range(len(PSPLIB_BENCH)):
            t = PSPLIB_BENCH[i]
            x, y = d[t]
            axslist[i].plot(x, y, label=b.name)
    for i in range(len(PSPLIB_BENCH)):
        t = PSPLIB_BENCH[i]
        axslist[i].set_title(t)
        axslist[i].grid()
        axslist[i].legend()
        axslist[i].set_ylim([0, 1])

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputfile, bbox_inches='tight')


def graph_best_so_far_init(data, title: str, outputfile):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(len(data), len(PSPLIB_BENCH), sharex="col", sharey="row")
    # fig.suptitle(title)
    fig.set_figwidth(10)
    fig.set_figheight(6)
    best_dict = load_bounds(os.path.join(DIR_DATA_PREPROCESSED, "bounds.txt"))
    for i in range(len(GENERATION_TIMES)):
        for j in range(len(PSPLIB_BENCH)):
            t = PSPLIB_BENCH[j]
            x = [0] + [p for p in [best_dict[k]['ub'] for k in best_dict if k.startswith(t)] if p >= 0]
            x.sort()
            y = [p / (PSPLIB_BENCH_GROUP[PSPLIB_BENCH[j]] * 10) for p in list(range(len(x)))]
            axs[i, j].plot(x, y, 'k', label="UB", linewidth=1)
        for b in data[GENERATION_TIMES[i]]:
            d = data[GENERATION_TIMES[i]][b].cactus_line_by_bench_best_all()
            for k in range(len(PSPLIB_BENCH)):
                t = PSPLIB_BENCH[k]
                x, y = d[t]
                axs[i, k].plot(x, y, label=data[GENERATION_TIMES[i]][b].name, linewidth=1)
        axs[i, 0].set_ylabel("TO={}sec\n% of instances".format(int(GENERATION_TIMES[i]/1000)), multialignment='center')
        axs[i, 0].set_ylim([0, 1])

    for j in range(len(PSPLIB_BENCH)):
        t = PSPLIB_BENCH[j]
        axs[0, j].set_title(t.upper())
        axs[len(data) - 1, j].set_xlabel("obj")
    for i in range(len(GENERATION_TIMES)):
        for j in range(len(PSPLIB_BENCH)):
            #axs[i, j].set_xscale('log')
            axs[i, j].grid()
            # axs[i, j].legend()
    axs[len(GENERATION_TIMES)-1,0].legend(loc='lower left')
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(outputfile, bbox_inches='tight')


def graph_best_so_far_grouped(bench: List[ResultRunSolver], grp, title: str, outputfile):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter
    fig, axs = plt.subplots(4, 4, sharex='col', sharey="row")
    # fig.suptitle(title)
    fig.set_figwidth(10)
    fig.set_figheight(7)
    for i in range(4):
        for j in range(4):
            axs[i, j].set_xscale('log')
            # axs[i,j].minorticks_off()
            # axs[i, j].set_ylabel("{} - % of instances".format(SUBSPLIT[i].upper()))
        axs[i, 0].set_ylabel("{}\n% of instances".format(SUBSPLIT[i].upper()))
    for j in range(4):
        axs[0, j].set_title(PSPLIB_BENCH[j].upper())
        axs[3, j].set_xlabel("obj")
        axs[3, j].xaxis.set_major_formatter(ScalarFormatter())
    best_dict = load_bounds(os.path.join(DIR_DATA_PREPROCESSED,"psplib", "bounds.txt"))
    for i in range(len(SUBSPLIT)):
        s = SUBSPLIT[i]
        for j in range(len(PSPLIB_BENCH)):
            t = PSPLIB_BENCH[j]
            x = [0] + [p for p in [best_dict[k]['ub'] for k in grp[s][t]] if p >= 0]
            x.sort()
            y = [p / len(grp[s][t]) for p in list(range(len(x)))]
            axs[i, j].plot(x, y, 'k', label="UB", linewidth=1)
        for b in bench:
            d = b.cactus_line_by_bench_best(grp[s])
            for k in range(len(PSPLIB_BENCH)):
                t = PSPLIB_BENCH[k]
                x, y = d[t]
                axs[i, k].plot(x, y, label=b.name, linewidth=1)
        for j in range(len(PSPLIB_BENCH)):
            axs[i, j].grid()
            # axs[i, j].legend()
            axs[i, j].set_ylim([0, 1])
        axs[i, 0].set_xticks([30, 40, 50, 60, 100, 200])
        axs[i, 1].set_xticks([60, 100])
        axs[i, 2].set_xticks([60, 100, 200, 300])
        axs[i, 3].set_xticks([100, 200, 300, 500])
    axs[len(GENERATION_TIMES)-1,0].legend(loc='lower left')

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(outputfile, bbox_inches='tight')


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
    best_dict = load_bounds(os.path.join(DIR_DATA_PREPROCESSED, "bounds.txt"))
    for i in range(len(PSPLIB_BENCH)):
        t = PSPLIB_BENCH[i]
        x = [0] + [t for t in [best_dict[k]['ub'] for k in best_dict if k.startswith(t)] if t >= 0]
        x.sort()
        y = [j / (PSPLIB_BENCH_GROUP[t] * 10) for j in list(range(len(x)))]
        axslist[i].plot(x, y, label="UB")
    for b in bench:
        d = b.cactus_line_by_bench_first()
        for i in range(len(PSPLIB_BENCH)):
            t = PSPLIB_BENCH[i]
            x, y = d[t]
            axslist[i].plot(x, y, label=b.name)
    for i in range(len(PSPLIB_BENCH)):
        t = PSPLIB_BENCH[i]
        axslist[i].set_title(t)
        axslist[i].grid()
        axslist[i].legend()
        # axslist[i].set_xlim([0, to])
        axslist[i].set_ylim([0, 1])

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outputfile, bbox_inches='tight')


if __name__ == "__main__":
    print("hello")
    results_to1s = ResultRunSolver(str(DIR_DATA_PREPROCESSED) + "/{}/{}_run_TO=1000_sbps=OFF.txt", "TO=1s", 1000)
    results_to1m = ResultRunSolver(str(DIR_DATA_PREPROCESSED) + "/{}/{}_run_TO=60000_sbps=OFF.txt", "TO=1m", 60000)

    graph_best_so_far([results_to1s, results_to1m], "testtitle", os.path.join(DIR_RESULTS_GRAPHS, "g.pdf"))
    graph_time([results_to1s, results_to1m], "testtitle", os.path.join(DIR_RESULTS_GRAPHS, "g_time.pdf"))
