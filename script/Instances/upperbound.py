# agregate all best solution from file
import math


def read_hrs(filename: str, bench: str, best_dict):
    with open(filename, encoding="utf-8") as file:
        lines = file.readlines()
        o = 4
        while o < len(lines) and lines[o][0].isdigit():
            line = lines[o].split()
            name = "{}{}_{}".format(bench, line[0], line[1])
            if name not in best_dict:
                best_dict[name] = {}
                best_dict[name]['ub'] = int(line[2])
                best_dict[name]["opt"] = False
            else:
                best_dict[name]['ub'] = min(int(line[2]), best_dict[name]['ub'])
                best_dict[name]['opt'] = 'lb' in best_dict[name] and best_dict[name]['lb'] == best_dict[name]['ub']
            o += 1


def read_opt(filename: str, bench: str, best_dict):
    with open(filename) as file:
        lines = file.readlines()
        o = 22
        while o < len(lines) and lines[o][0].isdigit():
            line = lines[o].split()
            name = "{}{}_{}".format(bench, line[0], line[1])
            if name not in best_dict:
                best_dict[name] = {}
            best_dict[name]['lb'] = int(line[2])
            best_dict[name]['ub'] = int(line[2])
            best_dict[name]["opt"] = True
            o += 1


def read_lb(filename: str, bench: str, best_dict):
    with open(filename) as file:
        lines = file.readlines()
        o = 0
        while o < len(lines) and not lines[o][0] == '=':
            o += 1
        o += 3
        while o < len(lines):
            line = lines[o].strip().split()
            if not line[0][0].isdigit():
                break
            name = "{}{}_{}".format(bench, line[0], line[1])
            if name not in best_dict:
                best_dict[name] = {}
                best_dict[name]['ub'] = int(line[2])
                best_dict[name]['lb'] = int(line[3])
            else:
                best_dict[name]['ub'] = min(int(line[2]), best_dict[name].get('ub', math.inf))
                best_dict[name]['lb'] = max(int(line[3]), best_dict[name].get('lb', -math.inf))
            best_dict[name]["opt"] = best_dict[name]['ub'] == best_dict[name]['lb']
            o += 1


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
