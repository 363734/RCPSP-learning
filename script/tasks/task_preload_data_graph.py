import os
import sys

from script.Instances.benchPSPLIB import read_arg_psplib
from script.logs import warning_log, title_log
from script.parameters import DIR_DATAS, DIR_DATA_PREPROCESSED

from script.Instances.RCPSPparser import parse_rcpsp, PSPLIB, log_trivial_precedences

if __name__ == "__main__":
    formatting = sys.argv[1]
    if formatting == PSPLIB:
        assert len(sys.argv) == 5
        bench, bench_group, instance_id = read_arg_psplib(sys.argv, 2)
        name = "{}{}_{}".format(bench, bench_group, instance_id)
        title_log("First reading (and pickleling) of file {} (psplib format) is there".format(name))
        data_file = os.path.join(DIR_DATAS, "psplib/{}/{}.sm".format(bench, name))
        inst = parse_rcpsp(data_file, PSPLIB) # parse the file, pickle it if first time read
        triv_prec_file = os.path.join(DIR_DATA_PREPROCESSED, "psplib/{}/{}_trivprec.txt".format(bench, name))
        log_trivial_precedences(inst, triv_prec_file) # log trivial precs
    else:  # TODO add new format here
        warning_log("Format {} is not supported for the RCPSP instance".format(formatting))
        exit(1)
