# Precedence graph data structure
from typing import List

import numpy as np


# data structure to model a precedence graph
class Graph:
    def __init__(self):
        self.map = {}  # store the node of the graph

    def nb_edges(self):
        return sum([len(self.map[k].idxs_s) for k in self.map])

    def nb_edges_transitive(self):
        return sum([len(self.map[k].idxs_s) for k in self.map])

    def nb_edges_transitive(self):
        return sum([len(self.map[k].idxs_s_all) for k in self.map])

    # add new node representing a task. Each node have an index (idx) and a duration (d)
    def add_node(self, idx: int):
        if idx not in self.map:
            self.map[idx] = Node(idx, self)

    # return the node of a given task index (idx)
    # the node should exist or else it will trigger an error
    def get(self, idx: int):
        return self.map[idx]

    # add new precedence: node index idx_p precedes node index idx_s
    # the nodes should exist or else it will trigger an error
    def add(self, idx_p: int, idx_s: int):
        self.get(idx_p).add_succ(idx_s)
        self.get(idx_s).add_prec(idx_p)

    # return true if adding the edge create a cycle
    def test_create_cycle(self, idx_p: int, idx_s: int):
        return self.get(idx_p).is_in_prec_all(idx_s) or self.get(idx_s).is_in_succ_all(idx_p)

    # construct an adjacency matrix (numpy matrix), where m[i,j] = 1 if i precedes j
    def get_adjacency_matrix(self):
        m = np.zeros((len(self.map), len(self.map)), dtype=float)
        for idx_p in self.map:
            for idx_s in self.map[idx_p].idxs_s:
                m[idx_p, idx_s] = 1
        return m

    def __str__(self):
        k = self.map.keys()

    def test_nodes(self):
        for n in self.map:
            out = self.get(n).test_node()
            if not out:
                return out
        return True


# data structure to model a node within the precedence graph
class Node:
    def __init__(self, idx: int, graph: Graph):
        self.idx = idx  # index of the node
        self.graph = graph  # graph in which the node belong
        self.idxs_p = []  # set of indexes of direct precedent
        self.idxs_s = []  # set of indexes of direct successor
        self.idxs_p_all = []  # set of all precedents (includes precedents of precedents,...)
        self.idxs_s_all = []  # set of all successors (includes successors of successors,...)

    def test_node(self):
        test = True
        for s in self.idxs_s:
            test &= s in self.idxs_s_all
            for ss in self.graph.get(s).idxs_s_all:
                test &= ss in self.idxs_s_all
        for p in self.idxs_p:
            test &= p in self.idxs_p_all
            for pp in self.graph.get(p).idxs_p_all:
                test &= pp in self.idxs_p_all
        return test

    def is_in_succ_all(self, candidate):
        return candidate in self.idxs_s_all

    def is_in_prec_all(self, candidate):
        return candidate in self.idxs_p_all

    # add new successor: node index idx_s succedes node index idx_p
    def add_succ(self, idx_s: int):
        if idx_s not in self.idxs_s:
            self.idxs_s.append(idx_s)  # add to the list of succ
            if idx_s not in self.idxs_s_all:
                for prec in [self.idx] + self.idxs_p_all:
                    for succ in [idx_s] + self.graph.get(idx_s).idxs_s_all:
                        if succ not in self.graph.get(prec).idxs_s_all:
                            self.graph.get(prec).idxs_s_all.append(succ)

    # add new precedence: node index idx_p precedes node index idx_s
    def add_prec(self, idx_p: int):
        if idx_p not in self.idxs_p:
            self.idxs_p.append(idx_p)
            if idx_p not in self.idxs_p_all:
                for succ in [self.idx] + self.idxs_s_all:
                    for prec in [idx_p] + self.graph.get(idx_p).idxs_p_all:
                        if prec not in self.graph.get(succ).idxs_p_all:
                            self.graph.get(succ).idxs_p_all.append(prec)


if __name__ == "__main__":

    g = Graph()
    for i in range(5):
        g.add_node(i, 0)
        print(g.test_nodes())
    g.add(0, 1)
    g.add(2, 3)
    g.add(3, 4)
    g.add(1, 2)
    print("----")
    print(g.test_nodes())
    for i in range(5):
        print(i)
        print(g.get(i).idxs_p)
        print(g.get(i).idxs_s)
        print(g.get(i).idxs_p_all)
        print(g.get(i).idxs_s_all)
    g.add(2, 4)
    g.add(1, 3)
    g.add(1, 3)
    print("----")
    print(g.test_nodes())
