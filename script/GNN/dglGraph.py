# create DGL graphs

import dgl
import torch

from script.Instances.RCPSPinstance import RCPSP
from script.Instances.RCPSPstats import get_stat
from typing import List


def get_dgl_graph(instance: RCPSP, with_trivial=True):
    stat = get_stat(instance)
    if with_trivial:
        s = instance.all_succ
    else:
        s = instance.successors
    nb_succ = sum([len(l) for l in s])
    x = [0] * nb_succ
    y = [0] * nb_succ
    k = 0
    for i in range(len(s)):
        for j in s[i]:
            x[k] = i
            y[k] = j
            k += 1
    graph = dgl.graph((x, y))
    # add features to nodes TODO features
    graph.ndata["usage"] = torch.tensor(stat.usage_proportion)
    graph.ndata["duration"] = torch.tensor(instance.duration)
    # graph.ndata["mean energy"] = torch.tensor([k/stat.mean_energy for k in stat.energy_per_job])
    # graph.ndata["feats"] = torch.tensor( #6 features
    #     [stat.usage_proportion[i] +[stat.usage_proportion_all[i]] + [instance.duration[i]] for i in range(len(stat.usage_proportion))])
    graph.ndata["feats"] = torch.tensor( #5 features
        [stat.usage_proportion[i] + [instance.duration[i]] for i in
         range(len(stat.usage_proportion))])
    return graph


def add_prec(graph, prec: List[List[int]]):
    x = [i[0] for i in prec]
    y = [i[1] for i in prec]
    return add_edges(graph,x, y)


def add_edges(graph, u, v):
    graph.add_edges(u, v)
    return graph

if __name__ == "__main__":

    graph = dgl.graph(([0,1,2],[3,4,5]))
    graph.add_edges([0],[3])