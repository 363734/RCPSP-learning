import os
import sys
import shutil


from script.Instances.PrecedenceParser import parse_precedence_multi, log_precedence
from script.Instances.benchPSPLIB import PSPLIB, read_arg_psplib
from script.logs import title_log, warning_log, step_log
from script.parameters import DIR_DATAS, DIR_DATA_PREPROCESSED_MULTI, DIR_DATA_PREPROCESSED


def aggregate(input_file: str, output_file: str, perc: float):
    precs = parse_precedence_multi(input_file)
    if len(precs) == 0:
        return False
    nb_graph = len(precs)
    agg = {}
    for prec in precs:
        for p in prec:
            agg[p] = agg.get(p, 0) + 1
    filtered_prec = []
    threshold = perc * nb_graph
    for key in agg:
        if agg[key] >= threshold:
            filtered_prec.append(key)
    step_log("nb sol {}, nb prec {}, and nb prec after filt {}".format(nb_graph, len(agg), len(filtered_prec)))
    log_precedence(output_file, filtered_prec)
    return True


if __name__ == "__main__":
    formatting = sys.argv[1]
    if formatting == PSPLIB:
        bench, bench_group, instance_id = read_arg_psplib(sys.argv, 2)
        name = "{}{}_{}".format(bench, bench_group, instance_id)
        opts = sys.argv[5]
        perc = float(sys.argv[6])
        opts_default = sys.argv[7]
        title_log("Aggregating file {} (psplib format) with solving options {} and threshold percentage of {}".format(name, opts, perc))
        input_file = os.path.join(
            DIR_DATA_PREPROCESSED_MULTI, PSPLIB, bench, "{}_allprec_multi_bsf_{}.txt".format(name, opts))
        output_file = os.path.join(
            DIR_DATA_PREPROCESSED_MULTI, PSPLIB, bench, "{}_allprec_bsf_{}_p={}.txt".format(name, opts, perc))
        if not aggregate(input_file, output_file, perc):
            #no multi-solution then copy unique solution
            step_log("no solution in multi, copying the one in single")
            one_solution_file = os.path.join(
                DIR_DATA_PREPROCESSED, PSPLIB, bench, "{}_allprec_bsf_{}.txt".format(name, opts_default, perc))
            shutil.copy2(one_solution_file, output_file)

    else:  # TODO add new format here
        warning_log("Format {} is not supported for the RCPSP instance".format(formatting))
        exit(1)
