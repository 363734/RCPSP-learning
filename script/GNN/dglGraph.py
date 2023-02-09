# create DGL graphs

import dgl
import torch

from script.Instances.RCPSPinstance import RCPSP
from script.Instances.RCPSPstats import get_stat


def get_dgl_graph(instance: RCPSP, withTrivial=True):
    stat = get_stat(instance)
    if withTrivial:
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
    return graph
