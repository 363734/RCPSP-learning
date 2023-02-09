import dgl

from script.GNN.dglGraph import get_dgl_graph
from script.Instances.RCPSPparser import parse_rcpsp
from script.PSPLIBinfo import BENCH, BENCH_GROUP

# step 1: get graphs
all_graphs = {}
all_graphs_dgl = {}
# for t in BENCH:
for t in ["j30"]:
    for i in range(1, BENCH_GROUP[t] + 1):
        for j in range(1, 11):
            name = "{}{}_{}".format(t, i, j)
            all_graphs[name] = parse_rcpsp("../../datas/{}/{}.sm".format(t, name)) #TODO add the + edges from solution + add trivial
            all_graphs_dgl[name] = get_dgl_graph(all_graphs[name])

print(all_graphs)
all_graphs_list = [all_graphs_dgl[k] for k in all_graphs_dgl]


# step 2: create batch
graph = dgl.batch(all_graphs_list)
print(graph)

