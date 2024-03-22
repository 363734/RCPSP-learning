import os.path
from math import floor

from script.GNN.prediction import prediction_parser
from script.Instances.benchPSPLIB import PSPLIB_BENCH, PSPLIB_BENCH_GROUP
from script.parameters import DIR_PREDICTIONS


def graph_hist_distribution_edge(files, title, labl, outputfile):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter
    fig, axs = plt.subplots(1, 1, sharex='col', sharey="row")
    fig.set_figwidth(4)
    fig.set_figheight(2)
    axs.set_ylabel("% of instances")
    axs.set_title(title.upper())
    axs.set_xlabel("predicted value")
    bins = [0] * 100
    for file in files:
        prec = prediction_parser(file)
        for p in prec:
            b = min(floor(p[2] / 0.01),len(bins)-1)
            bins[b] += 1
    xlab = [(i + 0.5) / 100 for i in range(0, 100, 1)]
    print(bins)
    total = sum(bins)
    bins = [i/total for i in bins]

    axs.set_axisbelow(True)
    axs.grid()
    axs.bar(xlab, bins, width=0.009, label=labl)
    axs.set_xlim([-0.01, 1.01])

    axs.legend(loc='upper right')

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(outputfile, bbox_inches='tight')


model = "sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=true_vsids=true]_0.01_bsfLoss"
bench = "j120"
d = os.path.join(DIR_PREDICTIONS, model)
files = [os.path.join(d, "pred_{}{}_{}_[{}].txt".format(bench, t, j, model)) for t in
         range(1, PSPLIB_BENCH_GROUP[bench] + 1) for j in range(1, 11)]
graph_hist_distribution_edge(files, bench, "Model B", "distri_{}_[{}].pdf".format(bench,model))
