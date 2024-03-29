import os

# times out (in ms) set for learning a close to optimal solution
GENERATION_TIMES = [1000, 60000, 600000, 3600000]
# GENERATION_TIMES = [3600000]

# percent of the positive edge as testing set:
# PERCENTAGE_TRAINING = ["20-80", "50-50", "80-20"]
KCROSSVALIDATION = 10

# in each bench, how many series are kept for validation (serie of 10 instance totally unseen by learning)
UNSEEN_SERIES = 5
# in each bench, in each seen series, how many instances are kept for validation (among the 10 of each series)
UNSEEN_WITHIN_SERIES = 2

## directory names
DIR_PROJECT = os.path.join(os.getcwd(), '..')
DIR_TARGET = os.path.join(DIR_PROJECT, "target")

DIR_SOLVER = os.path.join(DIR_PROJECT, "chuffed")
DIR_DATAS = os.path.join(DIR_TARGET, "datas")  # initial data from psplib
DIR_DATAS_PICKLE = os.path.join(DIR_TARGET, "datas_pickle")  # directory for pickle save of instance object
DIR_DATA_PREPROCESSED = os.path.join(DIR_TARGET,
                                     "datas_preprocessed")  # datas_preprocessed files (bounds, simple run, precedences files)
DIR_DATA_PREPROCESSED_MULTI = os.path.join(DIR_TARGET,
                                           "datas_preprocessed_multi")  # datas_preprocessed files (bounds, multi run, precedences files)
DIR_SPLIT = os.path.join(DIR_TARGET, "split")
DIR_SPLIT_MULTI = os.path.join(DIR_TARGET, "split_multi")
DIR_LOG_LEARNING = os.path.join(DIR_TARGET, "logs_learning")
DIR_LOG_LEARNING_MULTI = os.path.join(DIR_TARGET, "logs_learning_multi")
DIR_LOG_VALIDATION = os.path.join(DIR_TARGET, "logs_validation")
DIR_LOG_PREDICTION = os.path.join(DIR_TARGET, "logs_prediction")
DIR_LOG_ORDERING = os.path.join(DIR_TARGET, "logs_ordering")
DIR_RESULTS_GRAPHS = os.path.join(DIR_TARGET, "results_graphs")
DIR_TRAINED_MODELS = os.path.join(DIR_PROJECT, "trained_models")
DIR_PREDICTIONS = os.path.join(DIR_TARGET, "prediction")
DIR_RUN_RESULT = os.path.join(DIR_TARGET, "run_result")
DIR_RUN_RESULT_GREEDY = os.path.join(DIR_TARGET, "run_result_greedy")

DIR_LOG_LOCAL_SEARCH = os.path.join(DIR_TARGET, "logs_local_search")
DIR_RUN_LOCAL_SEARCH = os.path.join(DIR_TARGET, "run_local_search")

DIR = {"single": {
    "DATA_PREPROCESSED": DIR_DATA_PREPROCESSED,
    "SPLIT": DIR_SPLIT,
    "LOG_LEARNING": DIR_LOG_LEARNING
}, "multi": {
    "DATA_PREPROCESSED": DIR_DATA_PREPROCESSED_MULTI,
    "SPLIT": DIR_SPLIT_MULTI,
    "LOG_LEARNING": DIR_LOG_LEARNING_MULTI
}
}
