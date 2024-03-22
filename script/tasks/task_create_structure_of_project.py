import os
import sys

from script.Instances.benchPSPLIB import PSPLIB, PSPLIB_BENCH
from script.logs import *
from script.parameters import DIR_TARGET, DIR_DATAS, DIR_DATAS_PICKLE, DIR_DATA_PREPROCESSED, DIR_LOG_LEARNING, \
    DIR_RESULTS_GRAPHS, DIR_TRAINED_MODELS, DIR_LOG_VALIDATION, DIR_PREDICTIONS, DIR_RUN_RESULT, DIR_LOG_ORDERING, \
    DIR_LOG_PREDICTION, DIR_SPLIT, DIR_DATA_PREPROCESSED_MULTI

if __name__ == "__main__":
    if len(sys.argv) == 1:
        step_log("Creating structure of file")
        os.makedirs(DIR_TARGET, exist_ok=True)
        os.makedirs(DIR_DATAS, exist_ok=True)
        os.makedirs(DIR_DATAS_PICKLE, exist_ok=True)
        os.makedirs(DIR_DATA_PREPROCESSED, exist_ok=True)
        os.makedirs(DIR_DATA_PREPROCESSED_MULTI, exist_ok=True)
        os.makedirs(DIR_SPLIT, exist_ok=True)
        os.makedirs(DIR_LOG_LEARNING, exist_ok=True)
        os.makedirs(DIR_LOG_VALIDATION, exist_ok=True)
        os.makedirs(DIR_LOG_PREDICTION, exist_ok=True)
        os.makedirs(DIR_LOG_ORDERING, exist_ok=True)
        os.makedirs(DIR_RESULTS_GRAPHS, exist_ok=True)
        os.makedirs(DIR_TRAINED_MODELS, exist_ok=True)
        os.makedirs(DIR_PREDICTIONS, exist_ok=True)
        os.makedirs(DIR_RUN_RESULT, exist_ok=True)
    else:
        formatting = sys.argv[1]
        if formatting == PSPLIB:
            step_log("Creating structure of file for {} bench".format(formatting))
            os.makedirs(os.path.join(DIR_DATA_PREPROCESSED, formatting), exist_ok=True)
            os.makedirs(os.path.join(DIR_DATA_PREPROCESSED_MULTI, formatting), exist_ok=True)
            os.makedirs(os.path.join(DIR_SPLIT, formatting), exist_ok=True)
            for bench in PSPLIB_BENCH:
                os.makedirs(os.path.join(DIR_DATA_PREPROCESSED, formatting, bench), exist_ok=True)
                os.makedirs(os.path.join(DIR_DATA_PREPROCESSED_MULTI, formatting, bench), exist_ok=True)
        else:
            warning_log("Format {} is not supported for the RCPSP instance".format(formatting))
            exit(1)

