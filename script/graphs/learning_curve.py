import os

import numpy as np

from script.parameters import DIR_TARGET, DIR_LOG_LEARNING, DIR_RESULTS_GRAPHS


def parsing_learning_stats(filename: str):
    results = {"nb-epoch": 0}
    with open(filename) as file:
        lines = file.readlines()
        epoch = -1
        learning = True
        for line in lines:
            if line.startswith("epoch"):
                epoch = int(line[5:])
                if epoch not in results:
                    results[epoch] = {}
                    results["nb-epoch"] += 1
            elif "training" in line:
                train = "train"
            elif "testing" in line:
                train = "test"
            elif "Evaluation" in line:
                learning = False
                results["eval"] = {}
            elif "loss" in line:
                if learning:
                    results[epoch][train + "-loss"] = float(line[line.index(":") + 1:])
                else:
                    results["eval"][train + "-loss"] = float(line[line.index(":") + 1:])
            elif "auc" in line:
                if learning:
                    results[epoch][train + "-auc"] = float(line[line.index(":") + 1:])
                else:
                    results["eval"][train + "-auc"] = float(line[line.index(":") + 1:])
            elif "true pos" in line:
                if learning:
                    results[epoch][train + "-tp"] = float(line[line.index("(") + 1:line.index(")")])
                else:
                    results["eval"][train + "-tp"] = float(line[line.index("(") + 1:line.index(")")])
            elif "true neg" in line:
                if learning:
                    results[epoch][train + "-tn"] = float(line[line.index("(") + 1:line.index(")")])
                else:
                    results["eval"][train + "-tn"] = float(line[line.index("(") + 1:line.index(")")])
            elif "f1" in line:
                if learning:
                    results[epoch][train + "-f1"] = float(line[line.index(":") + 1:])
                else:
                    results["eval"][train + "-f1"] = float(line[line.index(":") + 1:])
            elif "precision" in line:
                if learning:
                    results[epoch][train + "-precision"] = float(line[line.index(":") + 1:])
                else:
                    results["eval"][train + "-precision"] = float(line[line.index(":") + 1:])
            elif "recall" in line:
                if learning:
                    results[epoch][train + "-recall"] = float(line[line.index(":") + 1:])
                else:
                    results["eval"][train + "-recall"] = float(line[line.index(":") + 1:])
    return results


def generate_graph(stats, outputfile: str):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(3, 1, sharex='col')
    fig.set_figwidth(10)
    fig.set_figheight(10)
    print(stats["nb-epoch"])
    x = list(range(0, stats["nb-epoch"]))
    axs[0].set_title("loss")
    axs[0].plot(x, [stats[i]["train-loss"] for i in x], label="train loss")
    axs[0].plot(x, [stats[i]["test-loss"] for i in x], label="test loss")
    axs[0].grid()
    axs[0].legend()
    axs[1].set_title("train accuracy")
    axs[1].set_ylim([0, 1])
    axs[1].set_yticks(np.arange(0, 1.05, step=0.05))
    # axs[1].plot(x, [stats[i]["train-tp"] for i in x], label="train tp")
    axs[1].plot(x, [stats[i]["train-tn"] for i in x], label="train tn")
    axs[1].plot(x, [stats[i]["train-f1"] for i in x], label="train f1")
    axs[1].plot(x, [stats[i]["train-precision"] for i in x], label="train precision")
    axs[1].plot(x, [stats[i]["train-recall"] for i in x], label="train recall")
    axs[1].grid()
    axs[1].legend()
    axs[2].set_title("test accuracy")
    axs[2].set_ylim([0, 1])
    axs[2].set_yticks(np.arange(0, 1.05, step=0.05))
    # axs[2].plot(x, [stats[i]["test-tp"] for i in x], label="test tp")
    axs[2].plot(x, [stats[i]["test-tn"] for i in x], label="test tn")
    axs[2].plot(x, [stats[i]["test-f1"] for i in x], label="test f1")
    axs[2].plot(x, [stats[i]["test-precision"] for i in x], label="test precision")
    axs[2].plot(x, [stats[i]["test-recall"] for i in x], label="test recall")
    axs[2].plot(x, [stats[i]["test-auc"] for i in x], label="test auc")
    axs[2].grid()
    axs[2].legend()

    plt.savefig(outputfile, bbox_inches='tight')


if __name__ == "__main__":
    # filename = os.path.join(DIR_LOG_LEARNING, "output_log_80-20_<=60_60000.txt")
    # stats = parsing_learning_stats(filename)
    # generate_graph(stats, os.path.join(DIR_RESULTS_GRAPHS, "learning_80-20_<=60_60000.pdf"))
    #
    # filename = os.path.join(DIR_LOG_LEARNING, "output_log_50-50_<=60_60000.txt")
    # stats = parsing_learning_stats(filename)
    # generate_graph(stats, os.path.join(DIR_RESULTS_GRAPHS, "learning_50-50_<=60_60000.pdf"))

    # filename = os.path.join(DIR_LOG_LEARNING, "output_log_80-20_<=60_60000_+prp.txt")
    # stats = parsing_learning_stats(filename)
    # generate_graph(stats, os.path.join(DIR_RESULTS_GRAPHS, "learning_80-20_<=60_60000_+prp.pdf"))

    filename = os.path.join(DIR_LOG_LEARNING, "output_log_80-20_<=60_60000_+prp+self.txt")
    stats = parsing_learning_stats(filename)
    generate_graph(stats, os.path.join(DIR_RESULTS_GRAPHS, "learning_80-20_<=60_60000_+prp+self.pdf"))

