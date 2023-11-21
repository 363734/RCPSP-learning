from script.Instances.benchPSPLIB import PSPLIB, split_bench_psplib, \
    split_instances_cross_psplib, split_cross_one_psplib, parse_rcpsp_psplib

mapfctformat = {
    PSPLIB: {"parse_rcpsp": parse_rcpsp_psplib,
             "split_bench": split_bench_psplib,
             "split_cross_one":split_cross_one_psplib,
             "split_instances_cross": split_instances_cross_psplib
            }
}
