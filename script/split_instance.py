import os

import torch

from script.GNN.dglGraph import get_dgl_graph, add_prec
from script.Instances.PrecedenceParser import parse_precedence
# from script.Instances.RCPSPparser import parse_rcpsp
from script.logs import step_log
from script.parameters import KCROSSVALIDATION
import numpy as np
import scipy.sparse as sp

from script.save_pickle_json import j_save, j_load
from script.select_prec import filter_precedence


def split_single_instance_test(outfile):
    if os.path.exists(outfile):
        step_log("Load from existing split")
        return j_load(outfile)
    else:
        return False


def split_single_instance(inst, prec_file, outfile, u_or_b: str):
    graph_dgl = get_dgl_graph(inst, True)  # TODO rm DGL from this function
    nb_edges_instance = graph_dgl.number_of_edges()
    precedences = filter_precedence(inst, parse_precedence(prec_file))
    graph_dgl = add_prec(graph_dgl, precedences)  # add just the new precedences

    u, v = graph_dgl.edges()
    eids = np.arange(
        graph_dgl.number_of_edges() - nb_edges_instance) + nb_edges_instance  # array with all ids from additionnal edges
    eids = np.random.permutation(eids)  # permutation

    # neg train/test
    u_bis = torch.cat((u, v[:nb_edges_instance]))  # not neg = neutral + pos, avoided (inverse of neutral)
    v_bis = torch.cat((v, u[:nb_edges_instance]))
    adj = sp.coo_matrix((np.ones(len(u_bis)), (u_bis.numpy(), v_bis.numpy())),
                        shape=(
                            graph_dgl.number_of_nodes(), graph_dgl.number_of_nodes()))  # compute adjacency matrix

    adj_neg = 1 - adj.todense() - np.eye(graph_dgl.number_of_nodes())  # invert adj matrix (without eye)
    neg_u, neg_v = np.where(adj_neg != 0)  # create vector of negative edges
    neg_eids = [k for k in range(len(neg_u))]
    neg_eids = np.random.permutation(neg_eids)

    if u_or_b == "uniform":
        step_log("performing uniform split")
        m = min(len(eids), len(neg_eids))
        eids = eids[:m]
        neg_eids = neg_eids[:m]
    else:
        step_log("performing {} split".format(u_or_b))

    idxstop_pos = [int(i * len(eids) / KCROSSVALIDATION) for i in range(KCROSSVALIDATION + 1)]
    cross_pos_u, cross_pos_v = [u[eids[idxstop_pos[i]:idxstop_pos[i + 1]]].tolist() for i in range(KCROSSVALIDATION)], [
        v[eids[idxstop_pos[i]:idxstop_pos[i + 1]]].tolist() for i in range(KCROSSVALIDATION)]
    cross_pos_u, cross_pos_v = [[int(k) for k in l] for l in cross_pos_u], [[int(k) for k in l] for l in cross_pos_v]

    idxstop_neg = [int(i * len(neg_eids) / KCROSSVALIDATION) for i in range(KCROSSVALIDATION + 1)]
    cross_neg_u, cross_neg_v = [list(neg_u[neg_eids[idxstop_neg[i]:idxstop_neg[i + 1]]]) for i in
                                range(KCROSSVALIDATION)], [
        list(neg_v[neg_eids[idxstop_neg[i]:idxstop_neg[i + 1]]]) for i in range(KCROSSVALIDATION)]
    cross_neg_u, cross_neg_v = [[int(k) for k in l] for l in cross_neg_u], [[int(k) for k in l] for l in
                                                                            cross_neg_v]

    step_log("finish computing crossval split")
    d = {"pos": (cross_pos_u, cross_pos_v),
         "neg": (cross_neg_u, cross_neg_v)}
    j_save(outfile, d)
    return d
