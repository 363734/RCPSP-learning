import os

import torch
import itertools
import numpy as np
import dgl.data
import time

from scripts.GNN.GraphNeuralNet import GraphSAGE
from scripts.GNN.MLPPredictor import MLPPredictor
from scripts.GNN.dglBatch import Batch
from scripts.GNN.dglGraph import get_dgl_graph
from scripts.GNN.metrics import compute_auc, compute_loss, compute_f1_score
from scripts.Instances.RCPSPparser import parse_rcpsp
from scripts.PSPLIBinfo import parse_bench_psplib
from scripts.parameters import DIR_PREPROCESSED, DIR_DATAS, DIR_TRAINED_MODELS
from scripts.split_bench import split_bench, split_instance


# TODO gérer le cas ou les usage sont pas les même

def learning(options):
    print("-" * 30)
    print("Step 1: get the training graph")
    split = split_bench(options.split_tag)
    btch = Batch(split)
    btch_seen = btch.get_batch("seen", parse_bench_psplib(options.psplib_batch))
    all_prec_file = "{}/{}_all_prec_optimal_solution_{}.txt"

    print(split)
    all_single_graphs = {}

    for t, i, j in btch_seen:
        name = "{}{}_{}".format(t, i, j)
        all_single_graphs[name] = {}
        print("Loading graph {}".format(name))
        inst = parse_rcpsp(os.path.join(DIR_DATAS, "{}/{}.sm".format(t, name)))
        graph = get_dgl_graph(inst, True)  # TODO check sans les trivial?
        all_single_graphs[name]["train"] = graph

        d = split_instance(options.split_tag, options.split_train_test, inst,
                           os.path.join(DIR_PREPROCESSED, all_prec_file.format(t, name, options.dataset_opts)))
        all_single_graphs[name]["train"].add_edges(d["train"]["pos"][0], d["train"]["pos"][1])

        all_single_graphs[name]["train-pos"] = dgl.graph((d["train"]["pos"][0], d["train"]["pos"][1]),
                                                         num_nodes=graph.number_of_nodes())
        all_single_graphs[name]["train-neg"] = dgl.graph((d["train"]["neg"][0], d["train"]["neg"][1]),
                                                         num_nodes=graph.number_of_nodes())

        all_single_graphs[name]["test-pos"] = dgl.graph((d["test"]["pos"][0], d["test"]["pos"][1]),
                                                        num_nodes=graph.number_of_nodes())
        all_single_graphs[name]["test-neg"] = dgl.graph((d["test"]["neg"][0], d["test"]["neg"][1]),
                                                        num_nodes=graph.number_of_nodes())

    train_graph = dgl.batch([all_single_graphs[k]["train"] for k in all_single_graphs])
    train_pos_g = dgl.batch([all_single_graphs[k]["train-pos"] for k in all_single_graphs])
    train_neg_g = dgl.batch([all_single_graphs[k]["train-neg"] for k in all_single_graphs])
    test_pos_g = dgl.batch([all_single_graphs[k]["test-pos"] for k in all_single_graphs])
    test_neg_g = dgl.batch([all_single_graphs[k]["test-neg"] for k in all_single_graphs])

    # ============================================================
    print("-" * 30)
    print("Step 2: Creation of the GNN, the predictor and optimizer")
    # model = GraphSAGE(3, "mean", train_graph.ndata['feats'].shape[1], 16)

    t_init_start = time.time()
    model = GraphSAGE(train_graph.ndata['feats'].shape[1], 16)

    pred = MLPPredictor(16)

    optimizer = torch.optim.Adam(itertools.chain(model.parameters(), pred.parameters()), lr=options.learning_rate)
    t_init_end = time.time()
    print("init_time (sec): {}".format(t_init_end - t_init_start))
    # ============================================================
    print("-" * 30)
    print("Step 3: Learning")
    t_learn = 0
    for e in range(options.epoch):
        print("-" * 15)
        print("epoch {}".format(e))

        t_learn_start = time.time()
        h = model(train_graph, train_graph.ndata['feats'])

        train_pos_score = pred(train_pos_g, h)
        train_neg_score = pred(train_neg_g, h)
        train_loss = compute_loss(train_pos_score, train_neg_score)
        train_tp = np.count_nonzero(np.greater_equal(train_pos_score.detach(), 0.))
        train_tn = np.count_nonzero(1 - np.greater_equal(train_neg_score.detach(), 0.))
        train_f1 = compute_f1_score(train_tp, len(train_neg_score) - train_tn, len(train_pos_score) - train_tp)

        test_pos_score = pred(test_pos_g, h)
        test_neg_score = pred(test_neg_g, h)
        test_loss = compute_loss(test_pos_score, test_neg_score)
        test_auc = compute_auc(test_pos_score.detach(), test_neg_score.detach())
        test_tp = np.count_nonzero(np.greater_equal(test_pos_score.detach(), 0.))
        test_tn = np.count_nonzero(1 - np.greater_equal(test_neg_score.detach(), 0.))
        test_f1 = compute_f1_score(test_tp, len(test_neg_score) - test_tn, len(test_pos_score) - test_tp)

        print("- training stats:")
        print("    * loss: {}".format(train_loss))
        print("    * true pos: {}/{} ({})".format(train_tp, len(train_pos_score), train_tp / len(train_pos_score)))
        print("    * true neg: {}/{} ({})".format(train_tn, len(train_neg_score), train_tn / len(train_neg_score)))
        print("    * f1 score: {}".format(train_f1))
        print("- testing stats:")
        print("    * loss: {}".format(test_loss))
        print("    * auc: {}".format(test_auc))
        print("    * true pos: {}/{} ({})".format(test_tp, len(test_pos_score), test_tp / len(test_pos_score)))
        print("    * true neg: {}/{} ({})".format(test_tn, len(test_neg_score), test_tn / len(test_neg_score)))
        print("    * f1 score: {}".format(test_f1))

        # backward
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

        if (e+1) % 25 == 0:
            filepath_GNN = os.path.join(DIR_TRAINED_MODELS, "mymodel_GNN_{}_epoch={}.pth".format(options.model_name,e+1))
            filepath_MLP = os.path.join(DIR_TRAINED_MODELS, "mymodel_MLP_{}_epoch={}.pth".format(options.model_name,e+1))
            torch.save(model.state_dict(), filepath_GNN)
            torch.save(pred.state_dict(), filepath_MLP)
            print("Models stored in files '{}' (GNN) and '{}' (MLP)".format(filepath_GNN, filepath_MLP))


    t_end = time.time()

    # ============================================================
    print("-" * 30)
    print("Step 4: Evaluation")
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

        test_pos_score = pred(test_pos_g, h)
        test_neg_score = pred(test_neg_g, h)
        test_loss = compute_loss(test_pos_score, test_neg_score)
        test_tp = np.count_nonzero(np.greater_equal(test_pos_score, 0.))
        test_tn = np.count_nonzero(1 - np.greater_equal(test_neg_score, 0.))
        test_auc = compute_auc(test_pos_score, test_neg_score)
        test_f1 = compute_f1_score(test_tp, len(test_neg_score) - test_tn, len(test_pos_score) - test_tp)

        print("- training stats:")
        print("    * loss: {}".format(train_loss))
        print("    * true pos: {}/{} ({})".format(train_tp, len(train_pos_score), train_tp / len(train_pos_score)))
        print("    * true neg: {}/{} ({})".format(train_tn, len(train_neg_score), train_tn / len(train_neg_score)))
        print("    * f1 score: {}".format(train_f1))
        print("- testing stats:")
        print("    * loss: {}".format(test_loss))
        print("    * auc: {}".format(test_auc))
        print("    * true pos: {}/{} ({})".format(test_tp, len(test_pos_score), test_tp / len(test_pos_score)))
        print("    * true neg: {}/{} ({})".format(test_tn, len(test_neg_score), test_tn / len(test_neg_score)))
        print("    * f1 score: {}".format(test_f1))

    # ============================================================
    print("=" * 30)
    print("Step 5: storing the model")
    filepath_GNN = os.path.join(DIR_TRAINED_MODELS, "mymodel_GNN_{}.pth".format(options.model_name))
    filepath_MLP = os.path.join(DIR_TRAINED_MODELS, "mymodel_MLP_{}.pth".format(options.model_name))
    torch.save(model.state_dict(), filepath_GNN)
    torch.save(pred.state_dict(), filepath_MLP)
    print("Models stored in files '{}' (GNN) and '{}' (MLP)".format(filepath_GNN, filepath_MLP))


if __name__ == "__main__":
    from scripts.option import parser

    args = ["--epoch=200", "--tt=80-20", "--ds-opts=TO=60000_sbps=OFF", "--lr=0.01","--model-name=80-20_<=60_60000_0.01_200"]
    (options, args) = parser.parse_args(args)
    print(options)
    learning(options)
