import os
import sys

from script.logs import warning_log
from script.parameters import KCROSSVALIDATION, DIR_TRAINED_MODELS

import shutil
import re


if __name__ == "__main__":

    file_pattern = sys.argv[1]
    output_file_bob = file_pattern.format("BEST") # bob = best of best

    id_best = -1
    value_best = 0

    for i in range(KCROSSVALIDATION):
        file_descr = os.path.join(DIR_TRAINED_MODELS, "mymodel_DESCR_{}.txt".format(file_pattern.format(i)))
        if os.path.exists(file_descr):
            with open(file_descr) as file:
                line = file.readlines()[0]
                reg_str = "<(.*?)>"
                res = re.findall(reg_str, line)
                value_i = float(res[0])
                print("cross {} found value {}".format(i, value_i))
                if value_i > value_best:
                    value_best = value_i
                    id_best = i
        else:
            warning_log("file not exist: {}".format(file_descr))

    if id_best == -1:
        print("WARNING SOMETHING WRONG, ONE SHOULD BE BETTER AT LEAST")
        exit(1)


    # copy the infos of the best file
    shutil.copy2(os.path.join(DIR_TRAINED_MODELS, "mymodel_GNN_{}.pth".format(file_pattern.format(id_best))),
                 os.path.join(DIR_TRAINED_MODELS, "mymodel_GNN_{}.pth".format(output_file_bob)))

    shutil.copy2(os.path.join(DIR_TRAINED_MODELS, "mymodel_MLP_{}.pth".format(file_pattern.format(id_best))),
                 os.path.join(DIR_TRAINED_MODELS, "mymodel_MLP_{}.pth".format(output_file_bob)))

    shutil.copy2(os.path.join(DIR_TRAINED_MODELS, "mymodel_DESCR_{}.txt".format(file_pattern.format(id_best))),
                 os.path.join(DIR_TRAINED_MODELS, "mymodel_DESCR_{}.txt".format(output_file_bob)))
