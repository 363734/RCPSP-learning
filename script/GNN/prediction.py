import os

import torch
import numpy as np
import scipy.sparse as sp
import dgl
# import torch.nn.functional as F

from script.GNN.dglGraph import get_dgl_graph
from script.GNN.model import load_model
from script.Instances.PrecedenceParser import log_precedence
from script.Instances.RCPSPparser import parse_rcpsp
from script.PSPLIBinfo import from_bench
from script.parameters import DIR_DATAS, DIR_TARGET


def predict(options):
    name = options.psplib_graph
    t = from_bench(name)
    inst = parse_rcpsp(os.path.join(DIR_DATAS, "{}/{}.sm".format(t, name)))
    graph = get_dgl_graph(inst, True)
    u, v = graph.edges()
    u_bis = torch.cat((u, v))
    v_bis = torch.cat((v, u))
    adj = sp.coo_matrix((np.ones(len(u_bis)), (u_bis.numpy(), v_bis.numpy())),
                        shape=(graph.number_of_nodes(), graph.number_of_nodes()))
    adj_neg = 1 - adj.todense() - np.eye(graph.number_of_nodes())
    neg_u, neg_v = np.where(adj_neg != 0)
    candidate = dgl.graph((neg_u, neg_v), num_nodes=graph.number_of_nodes())
    print(candidate)

    model, pred = load_model(options.model_name, graph)
    with torch.no_grad():
        h = model(graph, graph.ndata['feats'])
        candidate_score = torch.sigmoid(pred(candidate, h))
        # print(candidate_score)
        tp = np.count_nonzero(np.greater_equal(candidate_score.detach(), 0.5))
        print(len(candidate_score))
        print(tp)
        tp_75 = np.count_nonzero(np.greater_equal(candidate_score.detach(), 0.75))
        print(tp_75)
        all = [(candidate_score[i].item(), neg_u[i], neg_v[i]) for i in range(len(neg_u))]
        filter = [k for k in all if k[0] > 0.75]
        print(filter)
        filter = sorted(filter, reverse=True)
        print(filter)
        print(len(filter))
        prec_graph = inst.graph
        final = []
        for v,i,j in filter:
            # print(i,j)
            if not prec_graph.test_create_cycle(i,j):
                prec_graph.add(i,j,False)
                final.append((v,i,j))
        prec_list = [[i,j] for v,i,j in final]
        print(len(prec_list))
        log_precedence(os.path.join(DIR_TARGET,"prectest_{}.txt".format(options.psplib_graph)),prec_list)

        instfile = os.path.join(DIR_DATAS, "{}/{}.sm".format(t, name))
        precfile = os.path.join(DIR_TARGET,"prectest_{}.txt".format(options.psplib_graph))
        os.system(
            "../../chuffed/rcpsp-psplib {} ttef :prec {} :sbps -t 1000 > outtest.txt".format(instfile,precfile))

if __name__ == "__main__":
    from script.option import parser

    args = ["--mode=prediction","--psplib-graph=j6013_1"]
    (options, args) = parser.parse_args(args)
    print(options)
    predict(options)
