import sys

from script.graphs.learning_curve import parsing_learning_stats, generate_graph

if __name__ == "__main__":
    logfile = sys.argv[1]
    outfile = sys.argv[2]

    result = parsing_learning_stats(logfile)

    generate_graph(result, outfile)
