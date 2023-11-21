# # file gathering all the tasks to run
# import os
# from typing import List
#
# from script.PSPLIBinfo import BENCH, BENCH_GROUP
# from script.Instances.RCPSPparser import parse_rcpsp, PSPLIB, log_trivial_precedences
#
#
#
#
#
# # generate all files I_trivial_prec.txt
# def generate_trivial_prec():
#     for t in BENCH:
#         for i in range(1, BENCH_GROUP[t] + 1):
#             for j in range(1, 11):
#                 name = "{}{}_{}".format(t, i, j)
#                 print(name)
#                 inst = parse_rcpsp("./datas/{}/{}.sm".format(t, name), PSPLIB)
#                 log_trivial_precedences(inst, "./datas_preprocessed/{}/{}_trivial_prec.txt".format(t, name))
#
#
# def generate_prec_optimal(time_out: int):
#     for t in ["j30"]:  # BENCH:
#         # for i in range(1, BENCH_GROUP[t] + 1):
#         for i in range(9,10):
#             for j in range(1, 11):
#                 name = "{}{}_{}".format(t, i, j)
#                 print(name)
#                 # inst = parse_rcpsp("../datas/{}/{}.sm".format(t, name), PSPLIB)
#                 os.system(
#                     "../chuffed/rcpsp-psplib ../datas/{}/{}.sm ttef :print_prec_opti ../datas_preprocessed/{}/{}_all_prec_optimal_solution_TO={}_sbps=OFF.txt -t {}> ../datas_preprocessed/{}/{}_run_TO={}_sbps=OFF.txt".format(
#                         t, name, t, name, time_out, time_out, t, name, time_out))
#
#
# if __name__ == "__main__":
#     print("run")
#     # generate_trivial_prec()
#     # generate_prec_optimal(1000)
#     generate_prec_optimal(60000)
#
# # % Time limit exceeded!
