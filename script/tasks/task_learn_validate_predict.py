from script.GNN.prediction import predict

from script.GNN.evaluation import evaluation

from script.GNN.learning import learning
from script.logs import title_log, step_log, warning_log
from script.option import parser

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    if options.mode == "learning":
        title_log("=" * 30)
        title_log("=" * 30)
        title_log("Starting learning with options:")
        step_log("\t- K crossvalidation: {}".format(options.kcross))
        step_log("\t- Nb of epoch: {}".format(options.epoch))
        step_log("\t- Learning rate: {}".format(options.learning_rate))
        step_log("\t- Learning on dataset from PSPLIB: {}".format(options.psplib_batch))
        step_log("\t- Dataset created with parameters: {}".format(options.dataset_opts))
        step_log("\t- Dataset split id: {}".format(options.split_tag))
        step_log("\t- Name of the stored file for the model: {}".format(options.model_name))
        title_log("=" * 30)
        title_log("=" * 30)
        learning(options)
    elif options.mode == "evaluation":
        title_log("=" * 30)
        title_log("=" * 30)
        title_log("Starting evaluation with options:")
        step_log("\t- Model: {}".format(options.model_name))
        step_log("\t- Evaluation on dataset from PSPLIB: {}".format(options.psplib_batch))
        step_log("\t- Dataset created with parameters: {}".format(options.dataset_opts))
        step_log("\t- Part of dataset: {}".format(options.subbatch))
        step_log("\t- Dataset split id: {}".format(options.split_tag))
        title_log("=" * 30)
        title_log("=" * 30)
        evaluation(options)
    elif options.mode == "prediction":
        title_log("=" * 30)
        title_log("=" * 30)
        title_log("Starting prediction with options:")
        step_log("\t- Model: {}".format(options.model_name))
        step_log("\t- Graph from PSPLIB: {}".format(options.psplib_graph))
        predict(options)
    else:
        warning_log("Option --mode not accepted. Choose either 'learning', 'evaluation', 'prediction'")

