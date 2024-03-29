import os.path

from script.Instances.benchPSPLIB import PSPLIB_BENCH


def parsing_validation_stats_safe(filename: str):
    if os.path.exists(filename):
        return parsing_validation_stats(filename)
    else:
        return {"loss": -1, "tp": -1, "tn": -1, "f1": -1, "precision": -1, "recall": -1}


def parsing_validation_stats(filename: str):
    results = {"loss": -1, "tp": -1, "tn": -1, "f1": -1, "precision": -1, "recall": -1}
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            if "loss" in line:
                results["loss"] = float(line[line.rindex(":") + 1:])
            elif "true pos" in line:
                results["tp"] = float(line[line.rindex("(") + 1:line.rindex(")")])
            elif "true neg" in line:
                results["tn"] = float(line[line.rindex("(") + 1:line.rindex(")")])
            elif "f1" in line:
                results["f1"] = float(line[line.rindex(":") + 1:])
            elif "precision" in line:
                results["precision"] = float(line[line.rindex(":") + 1:])
            elif "recall" in line:
                results["recall"] = float(line[line.rindex(":") + 1:])
    print(filename)
    print(results)
    return results


def tab_validation(patternfile: str, outputfile: str):
    with open(outputfile, 'w') as table:
        table.write("\\documentclass[crop]{standalone}\n")
        table.write("\\usepackage{booktabs}\n")
        table.write("\\usepackage{multirow}\n")
        table.write("\\begin{document}\n")
        table.write("\\begin{tabular}{c||cccc||cccc||cccc||cccc}\n")
        table.write("\\toprule\n")
        table.write(
            "& f1 & prec & rec & tn & f1 & prec & rec & tn & f1 & prec & rec & tn & f1 & prec & rec & tn \\\\\n")
        table.write("\\midrule\n")
        for seen in ["seen", "unseen", "unknown","all"]:
            table.write("\\midrule\n")
            table.write(
                "Learning set & \\multicolumn{4}{c||}{"+seen+" $j30$}& \\multicolumn{4}{c||}{"+seen+" $j60$}& \\multicolumn{4}{c||}{"+seen+" $j90$}& \\multicolumn{4}{c}{"+seen+" $j120$} \\\\\n")
            for t in PSPLIB_BENCH:
                table.write("\\midrule\n")
                table.write("SEEN-$\leq$" + t)
                for t2 in PSPLIB_BENCH:
                    stat = parsing_validation_stats_safe(patternfile.format(t, t2, seen))
                    table.write("& {:.2f} & {:.2f} & {:.2f} & {:.2f}".format(stat["f1"], stat["precision"], stat["recall"], stat["tn"]))
                table.write("\\\\\n")
        table.write("\\bottomrule\n")
        table.write("\\end{tabular}\n")
        table.write("\\end{document}\n")
