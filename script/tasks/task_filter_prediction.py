import os.path
import sys

from script.PSPLIBinfo import from_bench

from script.parameters import DIR_DATAS

from script.Instances.RCPSPparser import parse_rcpsp

from script.Instances.PrecedenceParser import log_precedence

from script.GNN.prediction import prediction_parser

if __name__ == "__main__":
    assert len(sys.argv) == 3

    filename = sys.argv[1]
    threshold = float(sys.argv[2])
    direct, file = os.path.split(filename)
    f = str(file)
    idx0 = f.index("_")
    idx1 = f.index("[")
    outputfile = "prec{}{}_{}".format(f[idx0:idx1], threshold, f[idx1:])
    instancename = f[idx0 + 1:idx1 - 1]
    bench = from_bench(instancename)
    inst = parse_rcpsp(os.path.join(DIR_DATAS, "{}/{}.sm".format(bench, instancename)))

    prec = prediction_parser(filename)
    filter = [[l[0], l[1]] for l in prec if l[2] >= threshold]

    prec_graph = inst.graph
    final = []
    for l in filter:
        if not prec_graph.test_create_cycle(l[0], l[1]):
            prec_graph.add(l[0], l[1])
            final.append(l)

    log_precedence(os.path.join(direct, outputfile), final)
