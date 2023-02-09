from script.Instances.RCPSPinstance import RCPSP
from script.Instances.PrecedenceParser import parse_precedence, log_precedence
from typing import List


# remove the precedence from the list already in the graph
def filter_precedence(instance: RCPSP, prec: List[List[int]]) -> List[List[int]]:
    all_successors = instance.all_succ
    return [p for p in prec if not p[1] in all_successors[p[0]]]


#
def print_additional(output_file: str, instance: RCPSP, prec: List[List[int]]):
    nb = len(prec)
    print(nb)
    import random
    for x in range(10):
        for i in list(range(1, 10)) + list(range(10, 101, 5)):
            random.shuffle(prec)
            add_sub = prec[:nb * i // 100]
            log_precedence(output_file.format(i, x), add_sub)


if __name__ == "__main__":
    from script.Instances.RCPSPparser import parse_rcpsp, PSPLIB, log_trivial_precedences

    inst = parse_rcpsp("../datas/j90/j906_3.sm", PSPLIB)
    log_trivial_precedences(inst,"../preprocessed/j90/j906_3_trivial_prec.txt")
    print_additional("../results/proofofconcept/j906_3/additionnal_prec_j906_3_{}percent_{}.txt", inst,
                     filter_precedence(inst, parse_precedence(
                         "../preprocessed/j90/j906_3_all_prec_optimal_solution.txt")))
