import os
import time

import torch
import numpy as np
import dgl.data

from script.GNN.dglBatch import Batch
from script.GNN.dglGraph import get_dgl_graph
from script.GNN.metrics import compute_loss, compute_f1_score, compute_precision, compute_recall
from script.GNN.model import load_model
from script.Instances.RCPSPparser import parse_rcpsp
from script.PSPLIBinfo import parse_bench_psplib
from script.parameters import DIR_DATAS, DIR_PREPROCESSED
from script.split_bench import split_bench, split_instance_cross


def evaluation(options):
    print("-" * 30)
    print("Step 1: get the graph")
    split = split_bench(options.split_tag)
    btch = Batch(split)
    btch_seen = btch.get_batch(options.subbatch, parse_bench_psplib(options.psplib_batch))
    all_prec_file = "{}/{}_all_prec_optimal_solution_{}.txt"

    print(split)
    all_single_graphs = {}

    for t, i, j in btch_seen:
        name = "{}{}_{}".format(t, i, j)
        all_single_graphs[name] = {}
        print("Loading graph {}".format(name))
        inst = parse_rcpsp(os.path.join(DIR_DATAS, "{}/{}.sm".format(t, name)))
        graph = get_dgl_graph(inst, True)
        all_single_graphs[name]["inst"] = graph

        d = split_instance_cross(options.split_tag, inst,
                           os.path.join(DIR_PREPROCESSED, all_prec_file.format(t, name, options.dataset_opts)))#TODO fix

        all_single_graphs[name]["test-pos"] = dgl.graph((d["test"]["pos"][0], d["test"]["pos"][1]),
                                                        num_nodes=graph.number_of_nodes())
        all_single_graphs[name]["test-neg"] = dgl.graph((d["test"]["neg"][0], d["test"]["neg"][1]),
                                                        num_nodes=graph.number_of_nodes())

    inst_graph = dgl.batch([all_single_graphs[k]["inst"] for k in all_single_graphs])
    test_pos_g = dgl.batch([all_single_graphs[k]["test-pos"] for k in all_single_graphs])
    test_neg_g = dgl.batch([all_single_graphs[k]["test-neg"] for k in all_single_graphs])

    # ============================================================
    print("-" * 30)
    print("Step 2: load the model {}".format(options.model_name))
    t_init_start = time.time()
    model, pred = load_model(options.model_name, inst_graph)
    t_init_end = time.time()
    print("init_time (sec): {}".format(t_init_end - t_init_start))

    with torch.no_grad():
        # ============================================================
        print("-" * 30)
        print("Step 3: evaluation")
        t_eval_start = time.time()
        h = model(inst_graph, inst_graph.ndata['feats'])

        pos_score = pred(test_pos_g, h)
        neg_score = pred(test_neg_g, h)
        loss = compute_loss(pos_score, neg_score)
        tp = np.count_nonzero(np.greater_equal(pos_score, 0.))
        tn = np.count_nonzero(1 - np.greater_equal(neg_score, 0.))
        f1 = compute_f1_score(tp, len(neg_score) - tn, len(pos_score) - tp)
        precision = compute_precision(tp, len(neg_score) - tn)
        recall = compute_recall(tp, len(pos_score) - tp)

        print("- evaluation stats:")
        print("    * loss: {}".format(loss))
        print("    * true pos: {}/{} ({})".format(tp, len(pos_score), tp / len(pos_score)))
        print("    * true neg: {}/{} ({})".format(tn, len(neg_score), tn / len(neg_score)))
        print("    * f1 score: {}".format(f1))
        print("    * precision score: {}".format(precision))
        print("    * recall score: {}".format(recall))
        t_eval_end = time.time()
        print("evaluation time (sec): {}".format(t_eval_end - t_eval_start))


if __name__ == "__main__":
    from script.option import parser

    args = ["--mode=evaluation", "--ds-opts=TO=60000_sbps=OFF","--model-name=80-20_<=60_60000_0.01_200","--subbatch=unknown"]
    (options, args) = parser.parse_args(args)
    print(options)
    evaluation(options)