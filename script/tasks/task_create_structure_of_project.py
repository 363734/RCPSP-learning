import os

from script.PSPLIBinfo import BENCH
from script.parameters import DIR_TARGET, DIR_DATAS, DIR_DATAS_SAVE, DIR_PREPROCESSED, DIR_SPLIT, DIR_LOG_LEARNING, \
    DIR_RESULTS_GRAPHS, DIR_TRAINED_MODELS, DIR_LOG_VALIDATION, DIR_PREDICTIONS, DIR_RUN_RESULT, DIR_LOG_ORDERING, \
    DIR_LOG_PREDICTION, DIR_SPLIT_CROSS

if __name__ == "__main__":
    os.makedirs(DIR_TARGET, exist_ok=True)
    os.makedirs(DIR_DATAS, exist_ok=True)
    os.makedirs(DIR_DATAS_SAVE, exist_ok=True)
    os.makedirs(DIR_PREPROCESSED, exist_ok=True)
    for bench in BENCH:
        os.makedirs(os.path.join(DIR_PREPROCESSED, bench), exist_ok=True)
    #os.makedirs(DIR_SPLIT, exist_ok=True)
    os.makedirs(DIR_SPLIT_CROSS, exist_ok=True)
    os.makedirs(DIR_LOG_LEARNING, exist_ok=True)
    os.makedirs(DIR_LOG_VALIDATION, exist_ok=True)
    os.makedirs(DIR_LOG_PREDICTION, exist_ok=True)
    os.makedirs(DIR_LOG_ORDERING, exist_ok=True)
    os.makedirs(DIR_RESULTS_GRAPHS, exist_ok=True)
    os.makedirs(DIR_TRAINED_MODELS, exist_ok=True)

    os.makedirs(DIR_PREDICTIONS, exist_ok=True)
    os.makedirs(DIR_RUN_RESULT, exist_ok=True)
