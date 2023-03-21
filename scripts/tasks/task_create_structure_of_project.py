import os

from scripts.parameters import DIR_TARGET, DIR_DATAS, DIR_DATAS_SAVE, DIR_PREPROCESSED, DIR_SPLIT, DIR_LOG_LEARNING, \
    DIR_RESULTS_GRAPHS

if __name__ == "__main__":
    os.makedirs(DIR_TARGET, exist_ok=True)
    os.makedirs(DIR_DATAS, exist_ok=True)
    os.makedirs(DIR_DATAS_SAVE, exist_ok=True)
    os.makedirs(DIR_PREPROCESSED, exist_ok=True)
    os.makedirs(DIR_SPLIT, exist_ok=True)
    os.makedirs(DIR_LOG_LEARNING, exist_ok=True)
    os.makedirs(DIR_RESULTS_GRAPHS, exist_ok=True)
