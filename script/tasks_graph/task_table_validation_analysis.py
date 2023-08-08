import os
import sys

from script.parameters import DIR_LOG_VALIDATION, DIR_RESULTS_GRAPHS

from script.graphs.validation_tables import tab_validation

if __name__ == "__main__":
    tagsplit = sys.argv[1]
    dsopt = sys.argv[2]
    lr = sys.argv[3]
    model = sys.argv[4]

    tab_validation(str(os.path.join(DIR_LOG_VALIDATION,
                                    "log_" + tagsplit + "_BEST_<={0}_[" + dsopt + "]_" + lr + model + "_{1}_{2}.txt")),
                   os.path.join(DIR_RESULTS_GRAPHS,
                                "validation_" + tagsplit + "_[" + dsopt + "]_" + lr + model + ".tex"))

    os.system("pdflatex {}".format(os.path.join(DIR_RESULTS_GRAPHS,
                                                "validation_" + tagsplit + "_[" + dsopt + "]_" + lr + model + ".tex")))
