import os

import torch
import numpy as np
import scipy.sparse as sp
import dgl

from script.GNN.dglGraph import get_dgl_graph
from script.GNN.model import load_model
from script.Instances.RCPSPparser import parse_rcpsp
from script.PSPLIBinfo import from_bench
from script.parameters import DIR_DATAS, DIR_PREDICTIONS


def predict(options):
    print("-" * 30)
    print("Step 1: get the graph")
    pred_dir = os.path.join(DIR_PREDICTIONS, options.model_name)
    os.makedirs(pred_dir, exist_ok=True)
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

    # ============================================================
    print("-" * 30)
    print("Step 2: load the model {}".format(options.model_name))
    model, pred = load_model(options.model_name, graph)
    with torch.no_grad():
        # ============================================================
        print("-" * 30)
        print("Step 3: prediction")
        h = model(graph, graph.ndata['feats'])
        candidate_score = torch.sigmoid(pred(candidate, h))

        all = [(candidate_score[i].item(), neg_u[i], neg_v[i]) for i in range(len(neg_u))]
        sorted(all, reverse=True)
        print(all)
        filename = "pred_{}_[{}]".format(name, options.model_name)
        print(filename)
        with open(os.path.join(pred_dir, filename), "w") as file:
            for score, node_u, node_v in all:
                file.write("{}\t{}\t{}\n".format(node_u + 1, node_v + 1,
                                                 score))  # the +1 is necessary because ids in psplib starts at 1


if __name__ == "__main__":
    from script.option import parser

    args = ["--mode=prediction", "--psplib-graph=j6013_1",
            "--model=split1_50-50_<=j120_[TO=600000_sbps=false_vsids=false]_0.001_bsf"]
    (options, args) = parser.parse_args(args)
    print(options)
    predict(options)
