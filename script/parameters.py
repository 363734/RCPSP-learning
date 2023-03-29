import os

# times out (in ms) set for learning a close to optimal solution
GENERATION_TIMES = [1000, 60000, 600000]

# percent of the positive edge as testing set:
PERCENTAGE_TRAINING = ["20-80", "50-50", "80-20"]

# in each bench, how many series are kept for validation (serie of 10 instance totally unseen by learning)
UNSEEN_SERIES = 5
# in each bench, in each seen series, how many instances are kept for validation (among the 10 of each series)
UNSEEN_WITHIN_SERIES = 2

## directory names
DIR_PROJECT = os.path.join(os.getcwd(), '..')
DIR_TARGET = os.path.join(DIR_PROJECT, "target")

DIR_SOLVER = os.path.join(DIR_PROJECT,"chuffed")
DIR_DATAS = os.path.join(DIR_TARGET, "datas")  # initial data from psplib
DIR_DATAS_SAVE = os.path.join(DIR_TARGET, "datas_save")  # directory for pickle save of instance object
DIR_PREPROCESSED = os.path.join(DIR_TARGET,
                                "preprocessed")  # preprocessed files (bounds, simple run, precedences files)
DIR_SPLIT = os.path.join(DIR_TARGET, "split")
DIR_LOG_LEARNING = os.path.join(DIR_TARGET, "logs_learning")
DIR_RESULTS_GRAPHS = os.path.join(DIR_TARGET, "results_graphs")
DIR_TRAINED_MODELS = os.path.join(DIR_PROJECT, "trained_models")


