import os
import random


import numpy as np
import scipy.sparse as sp
import torch

from script.GNN.dglGraph import get_dgl_graph, add_prec
from script.Instances.PrecedenceParser import parse_precedence
from script.Instances.RCPSPinstance import RCPSP
from script.Instances.RCPSPparser import parse_rcpsp
from script.PSPLIBinfo import BENCH, BENCH_GROUP, from_bench
from script.parameters import UNSEEN_SERIES, UNSEEN_WITHIN_SERIES, DIR_PREPROCESSED, DIR_DATAS, DIR_SPLIT
from script.save_pickle_json import j_save, j_load
from script.select_prec import filter_precedence


def split_bench(tag: str):
    name = "split_{}.json".format(tag)
    dir_name = os.path.join(DIR_SPLIT, tag)
    filename = os.path.join(dir_name, name)
    if os.path.exists(filename):
        print("Load from existing split ({})".format(tag))
        return j_load(filename)
    else:
        print("Creating new split ({})".format(tag))
        os.makedirs(dir_name, exist_ok=True)
        bench = {"tag": tag}
        for t in BENCH:
            bench[t] = {}
            bench_id = [str(k) for k in list(range(1, BENCH_GROUP[t] + 1))]
            random.shuffle(bench_id)
            bench[t]["unseen"] = bench_id[:UNSEEN_SERIES]
            bench[t]["seen"] = bench_id[UNSEEN_SERIES:]
            for v in bench[t]["seen"]:
                bench[t][v] = {}
                serie_id = [str(k) for k in list(range(1, 11))]
                random.shuffle(serie_id)
                bench[t][v]["unseen"] = serie_id[:UNSEEN_WITHIN_SERIES]
                bench[t][v]["seen"] = serie_id[UNSEEN_WITHIN_SERIES:]
        j_save(filename, bench)
        return bench


def split_instance(tag: str, split_train_test: str, inst: RCPSP, prec_file: str):
    param_tag = os.path.basename(prec_file)
    bench = from_bench(param_tag)
    name = "split_{}_{}_{}.json".format(tag, split_train_test, param_tag)
    dir_name = os.path.join(DIR_SPLIT, tag, bench)
    filename = os.path.join(dir_name, name)
    if os.path.exists(filename):
        print("Load from existing split")
        return j_load(filename)
    else:
        os.makedirs(dir_name, exist_ok=True)
        perc = [int(k) / 100 for k in split_train_test.split("-")]
        graph_dgl = get_dgl_graph(inst, True)  # TODO rm DGL from this function
        nb_edges_instance = graph_dgl.number_of_edges()
        precedences = filter_precedence(inst, parse_precedence(prec_file))
        graph_dgl = add_prec(graph_dgl, precedences)

        u, v = graph_dgl.edges()
        eids = np.arange(graph_dgl.number_of_edges() - nb_edges_instance) + nb_edges_instance  # array with all ids
        eids = np.random.permutation(eids)  # permutation

        # pos train/test
        test_size = int(len(eids) * perc[1])  # test set
        # print(train_size)
        test_pos_u, test_pos_v = u[eids[:test_size]], v[
            eids[:test_size]]  # separation of the edges into train and test following permutation
        train_pos_u, train_pos_v = u[eids[test_size:]], v[eids[test_size:]]

        # neg train/test
        u_bis = torch.cat((u, v[:nb_edges_instance]))
        v_bis = torch.cat((v, u[:nb_edges_instance]))
        adj = sp.coo_matrix((np.ones(len(u_bis)), (u_bis.numpy(), v_bis.numpy())),
                            shape=(
                                graph_dgl.number_of_nodes(), graph_dgl.number_of_nodes()))  # compute adjacency matrix

        adj_neg = 1 - adj.todense() - np.eye(graph_dgl.number_of_nodes())  # invert adj matrix (without eye)
        neg_u, neg_v = np.where(adj_neg != 0)  # create vector of negative edges

        neg_eids = np.random.choice(len(neg_u),
                                    graph_dgl.number_of_edges())  # select randomly some ids of negative edge, same # as number of pos edge
        test_neg_u, test_neg_v = neg_u[neg_eids[:test_size]], neg_v[neg_eids[:test_size]]  # split test train
        train_neg_u, train_neg_v = neg_u[neg_eids[test_size:]], neg_v[neg_eids[test_size:]]

        print("not there")
        d = {"train": {"pos": (train_pos_u.tolist(), train_pos_v.tolist()), "neg": ([int(k) for k in list(train_neg_u)], [int(k) for k in list(train_neg_v)])},
             "test": {"pos": (test_pos_u.tolist(), test_pos_v.tolist()), "neg": ([int(k) for k in list(test_neg_u)], [int(k) for k in list(test_neg_v)])}}
        print(d)
        j_save(filename, d)
        return d


if __name__ == "__main__":
    # print(split_bench("0"))
    inst = parse_rcpsp(os.path.join(DIR_DATAS, "j30/j301_1.sm"))
    a = split_instance("0", "0-100", inst,
                       os.path.join(DIR_PREPROCESSED, "j30/j301_1_all_prec_optimal_solution_TO=1000_sbps=OFF.txt"))
    print(a)
