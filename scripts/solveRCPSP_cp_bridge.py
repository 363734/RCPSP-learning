import subprocess
import os



def run():
    #subprocess.run(["../chuffed/rcpsp-psplib", "../datas/j30/j301_1.sm","ttef"])
    # os.system("../chuffed/rcpsp-psplib ../datas/j30/j301_1.sm ttef > testfile.txt")
    # os.system("../chuffed/rcpsp-psplib ../datas/j90/j906_3.sm ttef > testfile_init.txt")
    os.system("../chuffed/rcpsp-psplib ../datas/j90/j906_3.sm ttef prec ./all_prec_optimal_j906_3.txt > testfile_initalloptimal.txt")
    # os.system("../chuffed/rcpsp-psplib ../datas/j90/j906_3.sm ttef prec ./trivial_prec_j906_3.txt > testfile_inittrivial.txt")
    # os.system("../chuffed/rcpsp-psplib ../datas/j906_3_m1.sm ttef > testfile_m1.txt")

def run_percent():
    for x in range(10):
        for i in list(range(1,10)) + list(range(10,101,5)):
            print(i)
            os.system(
                "../chuffed/rcpsp-psplib ../datas/j90/j906_3.sm ttef :prec ../results/proofofconcept/j906_3/additionnal_prec_j906_3_{}percent_{}.txt :sbps > ../results/proofofconcept/j906_3/solving_additionnal_prec_{}percent_{}.txt".format(i,x,i,x))

if __name__ == "__main__":
    print("tt")
    run_percent()
    print("end")