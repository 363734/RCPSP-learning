# ALL PSPLIB specifics
import os, math, random

from script.Instances.RCPSPinstance import RCPSP
from script.Instances.upperbound import save_bounds
from script.logs import step_log
from script.parameters import DIR_DATA_PREPROCESSED, DIR_DATAS, UNSEEN_SERIES, UNSEEN_WITHIN_SERIES, DIR_SPLIT, DIR
from script.split_instance import split_single_instance, split_single_instance_test

PSPLIB = "psplib"
PSPLIB_BENCH = ["j30", "j60", "j90", "j120"]
PSPLIB_BENCH_GROUP = {"j30": 48, "j60": 48, "j90": 48, "j120": 60}


# function to deduce the psplib benchmark the instance is from
def from_bench(name: str):
    for b in PSPLIB_BENCH:
        if b in name:
            return b


def read_arg_psplib(args, start: int):
    bench = args[start]  #
    bench_group = int(args[start + 1])
    instance_id = int(args[start + 2])
    return bench, bench_group, instance_id


# function to parse subset of psplib benchmark (e.g., <=j60 == j30 + j60)
def parse_bench_psplib(s: str):
    if s[:2] == "<=":
        return PSPLIB_BENCH[:PSPLIB_BENCH.index(s[2:]) + 1]
    elif s[:2] == ">=":
        return PSPLIB_BENCH[PSPLIB_BENCH.index(s[2:]):]
    elif s in PSPLIB_BENCH:
        return [s]
    else:
        print("PSPLIB benchmarck not well defined")
        print("use the name of one bench such as 'j60'")
        print("or '<=j60' to define all that are smaller too")
        print("or '>=j60' to define all that are greater too")
        exit(1)


# parse a file containing a RCPSP instance using the PSPLIB format
def parse_rcpsp_psplib(filename: str):
    with open(filename) as file:
        lines = file.readlines()
        nb_jobs = int(lines[5].split()[-1])
        successor = [[int(k) - 1 for k in line.strip().split()][3:] for line in lines[18:18 + nb_jobs]]
        info = [[int(k) for k in line.strip().split()][2:] for line in lines[18 + nb_jobs + 4:18 + 2 * nb_jobs + 4]]
        duration = [line[0] for line in info]
        usage = [line[1:] for line in info]
        resource = [int(k) for k in lines[-2].strip().split()]
        return RCPSP(nb_jobs, successor, duration, usage, resource)


def aggregate_bounds_psplib():
    step_log("Aggregating bounds for {}".format(PSPLIB))
    best_dict = {}
    for b in PSPLIB_BENCH:
        step_log("Aggregating bounds for {}: benchmark {}".format(PSPLIB, b))
        if b == 'j30':
            read_opt(os.path.join(DIR_DATAS, PSPLIB, "{}opt.sm".format(b)), b, best_dict)
            read_hrs(os.path.join(DIR_DATAS, PSPLIB, "{}hrs.sm".format(b)), b, best_dict)
        else:
            read_hrs(os.path.join(DIR_DATAS, PSPLIB, "{}hrs.sm".format(b)), b, best_dict)
            read_lb(os.path.join(DIR_DATAS, PSPLIB, "{}lb.sm".format(b)), b, best_dict)
    save_bounds(os.path.join(DIR_DATA_PREPROCESSED, PSPLIB, "bounds.txt"), best_dict)


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


def split_bench_psplib(bench):
    for t in PSPLIB_BENCH:
        bench[t] = {}
        bench_id = [str(k) for k in list(range(1, PSPLIB_BENCH_GROUP[t] + 1))]
        random.shuffle(bench_id)
        bench[t]["unseen"] = bench_id[:UNSEEN_SERIES]
        bench[t]["seen"] = bench_id[UNSEEN_SERIES:]
        for v in bench[t]["seen"]:
            bench[t][v] = {}
            serie_id = [str(k) for k in list(range(1, 11))]
            random.shuffle(serie_id)
            bench[t][v]["unseen"] = serie_id[:UNSEEN_WITHIN_SERIES]
            bench[t][v]["seen"] = serie_id[UNSEEN_WITHIN_SERIES:]
    return bench


def split_cross_one_psplib(name: str, precfileopt, tag, u_or_b: str, s_or_m: str = "single"):
    t = from_bench(name)
    file_inst = os.path.join(DIR_DATAS, "{}/{}/{}.sm".format(PSPLIB, t, name))
    prec_file = os.path.join(DIR[s_or_m]['DATA_PREPROCESSED'], "{}/{}/{}_{}.txt".format(PSPLIB, t, name, precfileopt))
    if os.path.exists(prec_file):
        step_log("Generate bench split for instance {}".format(name))
        dir_name = os.path.join(DIR[s_or_m]['SPLIT'], PSPLIB, tag)
        param_tag = os.path.basename(prec_file)
        name_out = "split_{}_{}.json".format(tag, param_tag)
        out_file = os.path.join(dir_name, name_out)
        o = split_single_instance_test(out_file)
        if o == False:
            print("Generate bench split for solution {}".format(prec_file))
            inst = parse_rcpsp_psplib(file_inst)
            o = split_single_instance(inst, prec_file, out_file, u_or_b)
        return o
    else:
        step_log("No prec file (and thus no generation): {}".format(prec_file))


def split_instances_cross_psplib(tag: str, precfileopt: str, u_or_b: str, s_or_m: str = "single"):
    for t in PSPLIB_BENCH:
        for i in range(1, PSPLIB_BENCH_GROUP[t] + 1):
            for j in range(1, 11):
                name = "{}{}_{}".format(t, i, j)
                split_cross_one_psplib(name, precfileopt, tag, u_or_b, s_or_m)
