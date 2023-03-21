from script.GNN.learning import learning
from script.option import parser

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    if options.mode == "learning":
        print("=" * 30)
        print("=" * 30)
        print("Starting learning with options:")
        print("\t- Train-test split: {}".format(options.split_train_test))
        print("\t- Nb of epoch: {}".format(options.epoch))
        print("\t- Learning rate: {}".format(options.learning_rate))
        print("\t- Learning on dataset from PSPLIB: {}".format(options.psplib_batch))
        print("\t- Dataset created with parameters: {}".format(options.dataset_opts))
        print("\t- Dataset split id: {}".format(options.split_tag))
        print("\t- Name of the stored file for the model: {}".format(options.model_name))
        print("=" * 30)
        print("=" * 30)
        learning(options)
    elif options.mode == "evaluation":
        print("=" * 30)
        print("=" * 30)
        print("Starting evaluation with options:")
        print("\t- Model: {}".format(options.model_name))
        print("\t- Dataset created with parameters: {}".format(options.dataset_opts))
        print("\t- Dataset split id: {}".format(options.split))
        print("=" * 30)
        print("=" * 30)
    elif options.mode == "prediction":
        print("prediction")
    else:
        print("Option --mode not accepted. Choose either 'learning', 'evaluation', 'prediction'")

