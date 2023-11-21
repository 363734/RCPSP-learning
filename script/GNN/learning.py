import math
import os

import torch
import itertools
import numpy as np
import dgl.data
import time

from script.GNN.GraphNeuralNet import GraphSAGE
from script.GNN.MLPPredictor import MLPPredictor
from script.GNN.dglBatch import Batch
from script.GNN.dglGraph import get_dgl_graph
from script.GNN.metrics import compute_loss, compute_f1_score, compute_precision, compute_recall
from script.Instances.RCPSPparser import parse_rcpsp
from script.Instances.bench import mapfctformat
from script.Instances.benchPSPLIB import parse_bench_psplib
from script.logs import step_log, title_log
from script.parameters import DIR_DATAS, DIR_TRAINED_MODELS
from script.split_bench import split_bench, split_extract_cross


def learning(options):
    title_log("-" * 30)
    title_log("Step 1: get the training graph k")
    split = split_bench(options.formatting, options.split_tag)
    btch = Batch(split)
    btch_seen = btch.get_batch("seen", parse_bench_psplib(options.psplib_batch))

    all_single_graphs = {}

    for t, i, j in btch_seen:
        name = "{}{}_{}".format(t, i, j)
        all_single_graphs[name] = {}
        step_log("Loading graph {}".format(name))
        inst = parse_rcpsp(os.path.join(DIR_DATAS, "psplib/{}/{}.sm".format(t, name)))
        graph = get_dgl_graph(inst, True)  # TODO check sans les trivial?
        all_single_graphs[name]["train"] = graph

        d = mapfctformat[options.formatting]["split_cross_one"](name, options.dataset_opts, options.split_cross_tag,
                                                                options.cross_type)

        kcross = options.kcross
        train_pos_u, test_pos_u = split_extract_cross(kcross, d["pos"][0])
        train_pos_v, test_pos_v = split_extract_cross(kcross, d["pos"][1])
        train_neg_u, test_neg_u = split_extract_cross(kcross, d["neg"][0])
        train_neg_v, test_neg_v = split_extract_cross(kcross, d["neg"][1])

        all_single_graphs[name]["train-pos"] = dgl.graph(([], []), num_nodes=graph.number_of_nodes())
        all_single_graphs[name]["train-neg"] = dgl.graph(([], []), num_nodes=graph.number_of_nodes())

        for cross_cut in range(len(train_pos_u)):
            all_single_graphs[name]["train"].add_edges(train_pos_u[cross_cut], train_pos_v[cross_cut])
            all_single_graphs[name]["train-pos"].add_edges(train_pos_u[cross_cut], train_pos_v[cross_cut])
        for cross_cut in range(len(train_neg_u)):
            all_single_graphs[name]["train-neg"].add_edges(train_neg_u[cross_cut], train_neg_v[cross_cut])

        all_single_graphs[name]["test-pos"] = dgl.graph((test_pos_u, test_pos_v),
                                                        num_nodes=graph.number_of_nodes())
        all_single_graphs[name]["test-neg"] = dgl.graph((test_neg_u, test_neg_v),
                                                        num_nodes=graph.number_of_nodes())

    train_graph = dgl.batch([all_single_graphs[k]["train"] for k in all_single_graphs])
    train_pos_g = dgl.batch([all_single_graphs[k]["train-pos"] for k in all_single_graphs])
    train_neg_g = dgl.batch([all_single_graphs[k]["train-neg"] for k in all_single_graphs])
    test_pos_g = dgl.batch([all_single_graphs[k]["test-pos"] for k in all_single_graphs])
    test_neg_g = dgl.batch([all_single_graphs[k]["test-neg"] for k in all_single_graphs])

    # ============================================================
    title_log("-" * 30)
    title_log("Step 2: Creation of the GNN, the predictor and optimizer")

    t_init_start = time.time()
    model = GraphSAGE(train_graph.ndata['feats'].shape[1], 16)

    pred = MLPPredictor(16)

    optimizer = torch.optim.Adam(itertools.chain(model.parameters(), pred.parameters()), lr=options.learning_rate)
    t_init_end = time.time()
    step_log("init_time (sec): {}".format(t_init_end - t_init_start))
    # ============================================================
    title_log("-" * 30)
    title_log("Step 3: Learning")
    t_learn_start = time.time()
    best_loss = math.inf
    for e in range(options.epoch):
        step_log("-" * 15)
        step_log("epoch {}".format(e))

        h = model(train_graph, train_graph.ndata['feats'])

        train_pos_score = pred(train_pos_g, h)
        train_neg_score = pred(train_neg_g, h)
        train_loss = compute_loss(train_pos_score, train_neg_score)
        train_tp = np.count_nonzero(np.greater_equal(train_pos_score.detach(), 0.))
        train_tn = np.count_nonzero(1 - np.greater_equal(train_neg_score.detach(), 0.))
        train_f1 = compute_f1_score(train_tp, len(train_neg_score) - train_tn, len(train_pos_score) - train_tp)
        train_precision = compute_precision(train_tp, len(train_neg_score) - train_tn)
        train_recall = compute_recall(train_tp, len(train_pos_score) - train_tp)

        test_pos_score = pred(test_pos_g, h)
        test_neg_score = pred(test_neg_g, h)
        test_loss = compute_loss(test_pos_score, test_neg_score)
        test_tp = np.count_nonzero(np.greater_equal(test_pos_score.detach(), 0.))
        test_tn = np.count_nonzero(1 - np.greater_equal(test_neg_score.detach(), 0.))
        test_f1 = compute_f1_score(test_tp, len(test_neg_score) - test_tn, len(test_pos_score) - test_tp)
        test_precision = compute_precision(test_tp, len(test_neg_score) - test_tn)
        test_recall = compute_recall(test_tp, len(test_pos_score) - test_tp)

        step_log("- training stats:")
        step_log("    * loss: {}".format(train_loss))
        step_log("    * true pos: {}/{} ({})".format(train_tp, len(train_pos_score), train_tp / len(train_pos_score)))
        step_log("    * true neg: {}/{} ({})".format(train_tn, len(train_neg_score), train_tn / len(train_neg_score)))
        step_log("    * f1 score: {}".format(train_f1))
        step_log("    * precision score: {}".format(train_precision))
        step_log("    * recall score: {}".format(train_recall))
        step_log("- testing stats:")
        step_log("    * loss: {}".format(test_loss))
        step_log("    * true pos: {}/{} ({})".format(test_tp, len(test_pos_score), test_tp / len(test_pos_score)))
        step_log("    * true neg: {}/{} ({})".format(test_tn, len(test_neg_score), test_tn / len(test_neg_score)))
        step_log("    * f1 score: {}".format(test_f1))
        step_log("    * precision score: {}".format(test_precision))
        step_log("    * recall score: {}".format(test_recall))

        if test_loss < best_loss:
            best_loss = test_loss
            filepath_GNN = os.path.join(DIR_TRAINED_MODELS,
                                        "mymodel_GNN_{}_bsfLoss.pth".format(options.model_name, e))
            filepath_MLP = os.path.join(DIR_TRAINED_MODELS,
                                        "mymodel_MLP_{}_bsfLoss.pth".format(options.model_name, e))
            torch.save(model.state_dict(), filepath_GNN)
            torch.save(pred.state_dict(), filepath_MLP)
            filepath_decript = os.path.join(DIR_TRAINED_MODELS,
                                            "mymodel_DESCR_{}_bsfLoss.txt".format(options.model_name, e))
            with open(filepath_decript, "w") as f_descript:
                f_descript.write("best model with Loss score of <{}> at epoch <{}>".format(best_loss, e))
            step_log("Models bsf-Loss from epoch {} stored in files '{}' (GNN) and '{}' (MLP)".format(e, filepath_GNN,
                                                                                                      filepath_MLP))

        # backward
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

    t_learn_end = time.time()
    step_log("learning time (sec): {}".format(t_learn_end - t_learn_start))
    # ============================================================
    title_log("-" * 30)
    title_log("Step 4: Evaluation")
    t_eval_start = time.time()
    with torch.no_grad():  # no gradient update since evaluation
        model.eval()
        pred.eval()
        h = model(train_graph, train_graph.ndata['feats'])

        train_pos_score = pred(train_pos_g, h)
        train_neg_score = pred(train_neg_g, h)
        train_loss = compute_loss(train_pos_score, train_neg_score)
        train_tp = np.count_nonzero(np.greater_equal(train_pos_score, 0.))
        train_tn = np.count_nonzero(1 - np.greater_equal(train_neg_score, 0.))
        train_f1 = compute_f1_score(train_tp, len(train_neg_score) - train_tn, len(train_pos_score) - train_tp)
        train_precision = compute_precision(train_tp, len(train_neg_score) - train_tn)
        train_recall = compute_recall(train_tp, len(train_pos_score) - train_tp)

        test_pos_score = pred(test_pos_g, h)
        test_neg_score = pred(test_neg_g, h)
        test_loss = compute_loss(test_pos_score, test_neg_score)
        test_tp = np.count_nonzero(np.greater_equal(test_pos_score, 0.))
        test_tn = np.count_nonzero(1 - np.greater_equal(test_neg_score, 0.))
        test_f1 = compute_f1_score(test_tp, len(test_neg_score) - test_tn, len(test_pos_score) - test_tp)
        test_precision = compute_precision(test_tp, len(test_neg_score) - test_tn)
        test_recall = compute_recall(test_tp, len(test_pos_score) - test_tp)

        step_log("- training stats:")
        step_log("    * loss: {}".format(train_loss))
        step_log("    * true pos: {}/{} ({})".format(train_tp, len(train_pos_score), train_tp / len(train_pos_score)))
        step_log("    * true neg: {}/{} ({})".format(train_tn, len(train_neg_score), train_tn / len(train_neg_score)))
        step_log("    * f1 score: {}".format(train_f1))
        step_log("    * precision score: {}".format(train_precision))
        step_log("    * recall score: {}".format(train_recall))
        step_log("- testing stats:")
        step_log("    * loss: {}".format(test_loss))
        step_log("    * true pos: {}/{} ({})".format(test_tp, len(test_pos_score), test_tp / len(test_pos_score)))
        step_log("    * true neg: {}/{} ({})".format(test_tn, len(test_neg_score), test_tn / len(test_neg_score)))
        step_log("    * f1 score: {}".format(test_f1))
        step_log("    * precision score: {}".format(test_precision))
        step_log("    * recall score: {}".format(test_recall))
    t_eval_end = time.time()
    step_log("evaluation time (sec): {}".format(t_eval_end - t_eval_start))

    # ============================================================
    title_log("=" * 30)
    title_log("Step 5: storing the model")
    filepath_GNN = os.path.join(DIR_TRAINED_MODELS, "mymodel_GNN_{}.pth".format(options.model_name))
    filepath_MLP = os.path.join(DIR_TRAINED_MODELS, "mymodel_MLP_{}.pth".format(options.model_name))
    torch.save(model.state_dict(), filepath_GNN)
    torch.save(pred.state_dict(), filepath_MLP)
    step_log("Models stored in files '{}' (GNN) and '{}' (MLP)".format(filepath_GNN, filepath_MLP))


if __name__ == "__main__":
    from script.option import parser

    args = ["--epoch=1000", "--tt=50-50", "--ds-opts=TO=600000_sbps=true_vsids=true", "--lr=0.001",
            "--model-name=50-50_<=120_60000_0.001_1000_TEST", "--psplib=<=j120"]
    (options, args) = parser.parse_args(args)
    print(options)
    learning(options)
