# agregate all best solution from file
import math


def save_bounds(output_file: str, best_dict):
    with open(output_file, 'w') as file:
        file.write("Inst\tUB\tLB\topt\n")
        for k in best_dict:
            ub = best_dict[k].get('ub', "-")
            lb = best_dict[k].get('lb', "-")
            if best_dict[k]['opt']:
                opt = "*"
            else:
                opt = "-"
            file.write("{}\t{}\t{}\t{}\n".format(k, ub, lb, opt))


# load the bounds for each instances from the aggegated file of bounds
def load_bounds(filename: str):
    best_dict = {}
    with open(filename) as file:
        lines = file.readlines()
        o = 1
        while o < len(lines) and lines[o][0] == 'j':
            line = lines[o].strip().split()
            best_dict[line[0]] = {}
            if line[1] != '-':
                best_dict[line[0]]['ub'] = int(line[1])
            if line[2] != '-':
                best_dict[line[0]]['lb'] = int(line[2])
            best_dict[line[0]]['opt'] = line[3] == '*'
            o += 1
    return best_dict
