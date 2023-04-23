import os
import sys

from script.parameters import DIR_DATAS, DIR_PREPROCESSED

from script.Instances.RCPSPparser import parse_rcpsp, PSPLIB, log_trivial_precedences

if __name__ == "__main__":
    assert len(sys.argv) == 4
    bench = sys.argv[1]
    bench_group = int(sys.argv[2])
    instance_id = int(sys.argv[3])
    name = "{}{}_{}".format(bench, bench_group, instance_id)
    print(name)
    data_file = os.path.join(DIR_DATAS, "{}/{}.sm".format(bench, name))
    inst = parse_rcpsp(data_file, PSPLIB)
    triv_prec_file = os.path.join(DIR_PREPROCESSED, "{}/{}_trivial_prec.txt".format(bench, name))
    log_trivial_precedences(inst, triv_prec_file)