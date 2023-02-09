# Precedence graph data structure
import numpy as np


# data structure to model a precedence graph
class Graph:
    def __init__(self):
        self.map = {}  # store the node of the graph

    # add new node representing a task. Each node have an index (idx) and a duration (d)
    def add_node(self, idx: int, d: int):
        if idx not in self.map:
            self.map[idx] = Node(idx, self, d)

    # return the node of a given task index (idx)
    # the node should exist or else it will trigger an error
    def get(self, idx: int):
        return self.map[idx]

    # add new precedence: node index idx_p precedes node index idx_s
    # the nodes should exist or else it will trigger an error
    def add(self, idx_p: int, idx_s: int):
        self.get(idx_s).add_prec(idx_p)

    # construct an adjacency matrix (numpy matrix), where m[i,j] = 1 if i precedes j
    def get_adjacency_matrix(self):
        m = np.zeros((len(self.map), len(self.map)), dtype=float)
        for idx_p in self.map:
            for idx_s in self.map[idx_p].idxs_s:
                m[idx_p, idx_s] = 1
        return m


# data structure to model a node within the precedence graph
class Node:
    def __init__(self, idx: int, graph: Graph, duration: int):
        self.idx = idx # index of the node
        self.graph = graph # graph in which the node belong
        self.duration = duration # duration of the task
        self.earliest_time = 0 # when does the task can start earliest
        self.latest_time = duration # horizon - latest_time is the latest it can start to finish the schedule
        self.idxs_p = [] # set of indexes of direct precedent
        self.idxs_s = [] # set of indexes of direct successor
        self.idxs_p_all = [] # set of all precedents (includes precedents of precedents,...)
        self.idxs_s_all = [] # set of all successors (includes successors of successors,...)

    # add new precedence: node index idx_p precedes node index idx_s
    def add_prec(self, idx_p: int):
        if idx_p in self.idxs_s:
            print("Warning, you are creating a cycle in your graph")
        node_p = self.graph.get(idx_p)
        if idx_p not in self.idxs_p:
            # update precedence link
            self.idxs_p.append(idx_p)
            self.add_all_prec([idx_p] + node_p.idxs_p_all)
            # update earliest time
            new_earliest = node_p.earliest_time + node_p.duration
            if new_earliest > self.earliest_time:
                self.earliest_time = new_earliest
                self.propagate_new_early()
        if self.idx not in node_p.idxs_s:
            # update successor link
            node_p.idxs_s.append(self.idx)
            node_p.add_all_succ([self.idx] + self.idxs_s_all)
            # update latest time
            new_latest = self.latest_time + node_p.duration
            if new_latest > node_p.latest_time:
                node_p.latest_time = new_latest
                node_p.propagate_new_latest()

    # propagate the earliest time of start
    def propagate_new_early(self):
        new_earliest = self.earliest_time + self.duration
        for s in self.idxs_s_all:
            if new_earliest > self.graph.get(s).earliest_time:
                self.graph.get(s).earliest_time = new_earliest
                self.graph.get(s).propagate_new_early()

    # propagate the latest start time to complete
    def propagate_new_latest(self):
        for p in self.idxs_p_all:
            new_latest = self.latest_time + self.graph.get(p).duration
            if new_latest > self.graph.get(p).latest_time:
                self.graph.get(p).latest_time = new_latest
                self.graph.get(p).propagate_new_latest()

    # update the list of all precedences (and propagate to the successors)
    def add_all_prec(self, idxs_p: int):
        for p in idxs_p:
            if p not in self.idxs_p_all:
                self.idxs_p_all.append(p)
        for s in self.idxs_s_all:
            self.graph.get(s).add_all_prec(idxs_p)

    # update the list of all successors (and propagate to the precedences)
    def add_all_succ(self, idxs_s: int):
        for s in idxs_s:
            if s not in self.idxs_s_all:
                self.idxs_s_all.append(s)
        for p in self.idxs_p_all:
            self.graph.get(p).add_all_succ(idxs_s)
