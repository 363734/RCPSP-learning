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
from script.PSPLIBinfo import parse_bench_psplib
from script.parameters import DIR_PREPROCESSED, DIR_DATAS, DIR_TRAINED_MODELS
from script.split_bench import split_bench, split_instance_cross, split_extract_cross


def learning(options):
    print("-" * 30)
    print("Step 1: get the training graph k")
    split = split_bench(options.split_tag)
    btch = Batch(split)
    btch_seen = btch.get_batch("seen", parse_bench_psplib(options.psplib_batch))
    all_prec_file = "{}/{}_all_prec_optimal_solution_{}.txt"

    all_single_graphs = {}

    for t, i, j in btch_seen:
        name = "{}{}_{}".format(t, i, j)
        all_single_graphs[name] = {}
        print("Loading graph {}".format(name))
        inst = parse_rcpsp(os.path.join(DIR_DATAS, "{}/{}.sm".format(t, name)))
        graph = get_dgl_graph(inst, True)  # TODO check sans les trivial?
        all_single_graphs[name]["train"] = graph

        d = split_instance_cross(options.split_tag, inst,
                                 os.path.join(DIR_PREPROCESSED, all_prec_file.format(t, name, options.dataset_opts)))

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
    print("-" * 30)
    print("Step 2: Creation of the GNN, the predictor and optimizer")

    t_init_start = time.time()
    model = GraphSAGE(train_graph.ndata['feats'].shape[1], 16)

    pred = MLPPredictor(16)

    optimizer = torch.optim.Adam(itertools.chain(model.parameters(), pred.parameters()), lr=options.learning_rate)
    t_init_end = time.time()
    print("init_time (sec): {}".format(t_init_end - t_init_start))
    # ============================================================
    print("-" * 30)
    print("Step 3: Learning")
    t_learn_start = time.time()
    best_f1 = 0
    best_precision = 0
    for e in range(options.epoch):
        print("-" * 15)
        print("epoch {}".format(e))

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

        print("- training stats:")
        print("    * loss: {}".format(train_loss))
        print("    * true pos: {}/{} ({})".format(train_tp, len(train_pos_score), train_tp / len(train_pos_score)))
        print("    * true neg: {}/{} ({})".format(train_tn, len(train_neg_score), train_tn / len(train_neg_score)))
        print("    * f1 score: {}".format(train_f1))
        print("    * precision score: {}".format(train_precision))
        print("    * recall score: {}".format(train_recall))
        print("- testing stats:")
        print("    * loss: {}".format(test_loss))
        print("    * true pos: {}/{} ({})".format(test_tp, len(test_pos_score), test_tp / len(test_pos_score)))
        print("    * true neg: {}/{} ({})".format(test_tn, len(test_neg_score), test_tn / len(test_neg_score)))
        print("    * f1 score: {}".format(test_f1))
        print("    * precision score: {}".format(test_precision))
        print("    * recall score: {}".format(test_recall))

        if test_f1 > best_f1:
            best_f1 = test_f1
            filepath_GNN = os.path.join(DIR_TRAINED_MODELS,
                                        "mymodel_GNN_{}_bsfF1.pth".format(options.model_name, e))
            filepath_MLP = os.path.join(DIR_TRAINED_MODELS,
                                        "mymodel_MLP_{}_bsfF1.pth".format(options.model_name, e))
            torch.save(model.state_dict(), filepath_GNN)
            torch.save(pred.state_dict(), filepath_MLP)
            filepath_decript = os.path.join(DIR_TRAINED_MODELS,
                                                "mymodel_DESCR_{}_bsfF1.pth".format(options.model_name, e))
            with open(filepath_decript, "w") as f_descript:
                f_descript.write("best model with F1 score of <{}> at epoch <{}>".format(best_f1, e))
            print("Models bsf-F1 from epoch {} stored in files '{}' (GNN) and '{}' (MLP)".format(e, filepath_GNN,
                                                                                              filepath_MLP))

        if test_precision > best_precision:
            best_precision = test_precision
            filepath_GNN = os.path.join(DIR_TRAINED_MODELS,
                                        "mymodel_GNN_{}_bsfPREC.pth".format(options.model_name, e))
            filepath_MLP = os.path.join(DIR_TRAINED_MODELS,
                                        "mymodel_MLP_{}_bsfPREC.pth".format(options.model_name, e))
            torch.save(model.state_dict(), filepath_GNN)
            torch.save(pred.state_dict(), filepath_MLP)
            filepath_decript = os.path.join(DIR_TRAINED_MODELS,
                                                "mymodel_DESCR_{}_bsfPREC.txt".format(options.model_name, e))
            with open(filepath_decript, "w") as f_descript:
                f_descript.write("best model with PREC score of <{}> at epoch <{}>".format(best_precision, e))
            print("Models bsf-PREC from epoch {} stored in files '{}' (GNN) and '{}' (MLP)".format(e, filepath_GNN,
                                                                                              filepath_MLP))


        # backward
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

        # if (e + 1) % 50 == 0:
        #     filepath_GNN = os.path.join(DIR_TRAINED_MODELS,
        #                                 "mymodel_GNN_{}_epoch={}.pth".format(options.model_name, e + 1))
        #     filepath_MLP = os.path.join(DIR_TRAINED_MODELS,
        #                                 "mymodel_MLP_{}_epoch={}.pth".format(options.model_name, e + 1))
        #     torch.save(model.state_dict(), filepath_GNN)
        #     torch.save(pred.state_dict(), filepath_MLP)
        #     print("Models stored in files '{}' (GNN) and '{}' (MLP)".format(filepath_GNN, filepath_MLP))

    t_learn_end = time.time()
    print("learning time (sec): {}".format(t_learn_end - t_learn_start))
    # ============================================================
    print("-" * 30)
    print("Step 4: Evaluation")
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

        print("- training stats:")
        print("    * loss: {}".format(train_loss))
        print("    * true pos: {}/{} ({})".format(train_tp, len(train_pos_score), train_tp / len(train_pos_score)))
        print("    * true neg: {}/{} ({})".format(train_tn, len(train_neg_score), train_tn / len(train_neg_score)))
        print("    * f1 score: {}".format(train_f1))
        print("    * precision score: {}".format(train_precision))
        print("    * recall score: {}".format(train_recall))
        print("- testing stats:")
        print("    * loss: {}".format(test_loss))
        print("    * true pos: {}/{} ({})".format(test_tp, len(test_pos_score), test_tp / len(test_pos_score)))
        print("    * true neg: {}/{} ({})".format(test_tn, len(test_neg_score), test_tn / len(test_neg_score)))
        print("    * f1 score: {}".format(test_f1))
        print("    * precision score: {}".format(test_precision))
        print("    * recall score: {}".format(test_recall))
    t_eval_end = time.time()
    print("evaluation time (sec): {}".format(t_eval_end - t_eval_start))

    # ============================================================
    print("=" * 30)
    print("Step 5: storing the model")
    filepath_GNN = os.path.join(DIR_TRAINED_MODELS, "mymodel_GNN_{}.pth".format(options.model_name))
    filepath_MLP = os.path.join(DIR_TRAINED_MODELS, "mymodel_MLP_{}.pth".format(options.model_name))
    torch.save(model.state_dict(), filepath_GNN)
    torch.save(pred.state_dict(), filepath_MLP)
    print("Models stored in files '{}' (GNN) and '{}' (MLP)".format(filepath_GNN, filepath_MLP))


if __name__ == "__main__":
    from script.option import parser

    args = ["--epoch=1000", "--tt=50-50", "--ds-opts=TO=600000_sbps=true_vsids=true", "--lr=0.001",
            "--model-name=50-50_<=120_60000_0.001_1000_TEST", "--psplib=<=j120"]
    (options, args) = parser.parse_args(args)
    print(options)
    learning(options)
