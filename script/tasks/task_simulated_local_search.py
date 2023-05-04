import math
import os
import random
import sys
import time
from typing import List

import dgl
import torch
import numpy as np
import scipy.sparse as sp
from script.select_prec import filter_precedence

from script.Instances.PrecedenceParser import log_precedence, parse_precedence

from script.GNN.dglGraph import get_dgl_graph

from script.GNN.model import load_model

from script.parameters import DIR_DATAS, DIR_LOG_LOCAL_SEARCH, DIR_SOLVER

from script.Instances.RCPSPparser import parse_rcpsp

from script.PSPLIBinfo import from_bench


def get_prediction(options, dglgraph):
    u, v = dglgraph.edges()
    u_bis = torch.cat((u, v))
    v_bis = torch.cat((v, u))
    adj = sp.coo_matrix((np.ones(len(u_bis)), (u_bis.numpy(), v_bis.numpy())),
                        shape=(dglgraph.number_of_nodes(), dglgraph.number_of_nodes()))
    adj_neg = 1 - adj.todense() - np.eye(dglgraph.number_of_nodes())
    neg_u, neg_v = np.where(adj_neg != 0)

    candidate = dgl.graph((neg_u, neg_v), num_nodes=dglgraph.number_of_nodes())

    print("load model: {}".format(options.model_name))
    model, pred = load_model(options.model_name, dglgraph)
    with torch.no_grad():
        h = model(dglgraph, dglgraph.ndata['feats'])
        candidate_score = torch.sigmoid(pred(candidate, h))

        all = [(candidate_score[i].item(), neg_u[i], neg_v[i]) for i in range(len(neg_u))]
        all = sorted(all, reverse=True)
        return all


def get_filtered_precedence(options, precadded, prectoadd):
    filter = [[l[1], l[2]] for l in prectoadd if l[0] >= options.threshold]

    name = options.psplib_graph
    t = from_bench(name)
    inst = parse_rcpsp(os.path.join(DIR_DATAS, "{}/{}.sm".format(t, name)))
    prec_graph = inst.graph
    for l in precadded:
        prec_graph.add(l[0], l[1])

    final = []
    for l in filter:
        if not prec_graph.test_create_cycle(l[0], l[1]):
            prec_graph.add(l[0], l[1])
            final.append(l)

    return final


def parse_result_onefile(filename):
    best = math.inf
    # time = -1
    with open(filename) as file:
        # print("reading stuff")
        lines = file.readlines()
        for k in range(len(lines)).__reversed__():
            if lines[k][:10] == "makespan =":
                if best == math.inf:
                    best = int(lines[k][10:])
            # if lines[k][:18] == "%%%mzn-stat: time=":
            #     time = float(lines[k][18:])
            # if lines[k][:22] == "% Time limit exceeded!":
            #     time = -1
    return best


def simulated_local_search(options):
    # ============================================================
    print("-" * 30)
    print("Step 1: Initialization")
    name = options.psplib_graph
    tag = "{}_{}_[{}]_{}_TO={}-{}_sbps={}_vsids={}".format(name, options.threshold, options.model_name, options.ls_keep,
                                                           options.to_round,
                                                           options.to_total, options.sbps, options.vsids)
    DIR_THIS_LS = os.path.join(DIR_LOG_LOCAL_SEARCH, options.model_name)
    os.makedirs(DIR_THIS_LS, exist_ok=True)
    t = from_bench(name)
    data_file = os.path.join(DIR_DATAS, "{}/{}.sm".format(t, name))
    inst = parse_rcpsp(data_file)
    endtime = time.time() * 1000 + options.to_total
    # ============================================================
    print("-" * 30)
    print("Step 2: First run (prediction from instance)")
    graph = get_dgl_graph(inst, True)
    print("- prediction:")
    prec = get_prediction(options, graph)
    print("- filter prediction:")
    prec_filtered = get_filtered_precedence(options, [], prec)
    train_prec = os.path.join(DIR_THIS_LS, "{}_prec_0.txt".format(tag))
    ordering_file = os.path.join(DIR_THIS_LS, "{}_orde_0.txt".format(tag))
    ordering_log_file = os.path.join(DIR_THIS_LS, "{}_orde_log_0.txt".format(tag))
    log_precedence(train_prec, prec_filtered)
    print("- create ordering:")
    os.system(
        '{}/rcpsp-ordering {} :add_prec "{}" :print_ordering "{}" > "{}"'.format(
            DIR_SOLVER, data_file, train_prec, ordering_file, ordering_log_file))
    print("- solving with ordering:")
    time_out = min(endtime - time.time() * 1000, options.to_round)
    new_prec_file = os.path.join(DIR_THIS_LS, "{}_prec_new_0.txt".format(tag))
    sol_file = os.path.join(DIR_THIS_LS, "{}_sol_0.txt".format(tag))
    os.system(
        '{}/rcpsp-psplib {} ttef :add_ordering "{}" :print_prec_opti "{}" --sbps {} --vsids {} -t {} > "{}"'.format(
            DIR_SOLVER, data_file, ordering_file, new_prec_file, options.sbps, options.vsids, time_out, sol_file))
    if not os.path.exists(new_prec_file):
        print("WARNING: your round time out is too small to generate a solution")
    last_new_prec_file = new_prec_file
    i = 0
    while time.time() * 1000 <= endtime or i >= options.to_total/options.to_round:
        i += 1
        # ============================================================
        print("-" * 30)
        print("Step 3 - loop {}: Loop".format(i))
        print("- verify prec last round:")
        if not os.path.exists(new_prec_file):
            print("WARNING: round {} didn't produce precedences, fallback to the previouly valid ones".format(i - 1))
        else:
            last_new_prec_file = new_prec_file
        print("Previous prec used in {}".format(last_new_prec_file))
        print("- sample precedences:")
        prev_prec = filter_precedence(inst, parse_precedence(new_prec_file))
        random.shuffle(prev_prec)
        prev_prec = prev_prec[:int(options.ls_keep * len(prev_prec))]
        graph = get_dgl_graph(inst, True)
        graph.add_edges([k[0] for k in prev_prec], [k[1] for k in prev_prec])
        print("- prediction:")
        prec = get_prediction(options, graph)
        print("- filter prediction:")
        prec_filtered = get_filtered_precedence(options, prev_prec, prec)

        train_prec = os.path.join(DIR_THIS_LS, "{}_prec_{}.txt".format(tag, i))
        ordering_file = os.path.join(DIR_THIS_LS, "{}_orde_{}.txt".format(tag, i))
        ordering_log_file = os.path.join(DIR_THIS_LS, "{}_orde_log_{}.txt".format(tag, i))
        log_precedence(train_prec, prec_filtered)

        print("- create ordering:")
        os.system(
            '{}/rcpsp-ordering {} :add_prec "{}" :print_ordering "{}" > "{}"'.format(
                DIR_SOLVER, data_file, train_prec, ordering_file, ordering_log_file))
        print("- solving with ordering:")
        time_out = min(endtime - time.time() * 1000, options.to_round)
        if time_out >= 1000: # no need to start the solver for less than 1 sec
            new_prec_file = os.path.join(DIR_THIS_LS, "{}_prec_new_{}.txt".format(tag, i))
            sol_file = os.path.join(DIR_THIS_LS, "{}_sol_{}.txt".format(tag, i))
            # os.system(
            #     '{}/rcpsp-psplib {} ttef :add_prec "{}" :add_ordering "{}" :print_prec_opti "{}" --sbps {} --vsids {} -t {} > "{}"'.format(
            #         DIR_SOLVER, data_file, train_prec, ordering_file, new_prec_file, options.sbps, options.vsids, time_out,
            #         sol_file))
            os.system(
                '{}/rcpsp-psplib {} ttef :add_ordering "{}" :print_prec_opti "{}" --sbps {} --vsids {} -t {} > "{}"'.format(
                    DIR_SOLVER, data_file, ordering_file, new_prec_file, options.sbps, options.vsids, time_out,
                    sol_file))

    print("=" * 30)
    print("Step 4: aggregate to Best sol")
    best = math.inf
    k = -1
    for j in range(0, i + 1):
        sol_file = os.path.join(DIR_THIS_LS, "{}_sol_{}.txt".format(tag, j))
        if os.path.exists(sol_file):
            new_res = parse_result_onefile(sol_file)
            print("Solution at round {} is: {}".format(j, new_res))
            if new_res < best:
                k = j
                best = new_res

    print("-" * 20)
    print("Best solution found at round {}: {}".format(k, best))


if __name__ == "__main__":
    from script.option_simulated_local_search import parser

    # args = ["--psplib-graph=j6013_1",  # UB = 112 -> found 115
    #         "--model-name=split2_20-80_<=j120_[TO=600000_sbps=true_vsids=true]_0.001_bsf", "--ls-keep=0.30",
    #         "--to-round=60000"]
    (options, args) = parser.parse_args()
    print(options)
    simulated_local_search(options)
