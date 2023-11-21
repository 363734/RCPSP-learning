import math
import os

from script.Instances.benchPSPLIB import PSPLIB_BENCH, PSPLIB_BENCH_GROUP


def parse_preprocessed_result(filename_pattern: str, caption_name: str, time_out: int):
    dict = {}
    for t in PSPLIB_BENCH:
        for i in range(1, PSPLIB_BENCH_GROUP[t] + 1):
            for j in range(1, 11):
                print("Read results for {}".format(filename_pattern.format(t, caption_name)))
                name = "{}{}_{}".format(t, i, j)
                if os.path.exists(filename_pattern.format(t, name)):
                    dict[name] = {}
                    with open(filename_pattern.format(t, name)) as file:
                        # print("reading stuff")
                        lines = file.readlines()
                        for k in range(len(lines)).__reversed__():
                            if lines[k][:10] == "makespan =" :
                                if 'best' not in dict[name]:
                                    dict[name]['best'] = int(lines[k][10:])
                                dict[name]['first'] = int(lines[k][10:])
                            if lines[k][:18] == "%%%mzn-stat: time=":
                                dict[name]['time'] = float(lines[k][18:])
                            # if lines[k][:19] == "%%%mzn-stat: nodes=":
                            #     node = int(lines[k][19:])
                            #     n.append(node)
                            if lines[k][:22] == "% Time limit exceeded!":
                                dict[name]['time'] = -1
    return ResultRunSolver(caption_name, time_out, dict)


def parse_result_final(filename_pattern: str, caption_name: str, time_out: int):
    dict = {}
    for t in PSPLIB_BENCH:
        for i in range(1, PSPLIB_BENCH_GROUP[t] + 1):
            for j in range(1, 11):
                print("Read results for {}".format(filename_pattern.format(caption_name)))
                name = "{}{}_{}".format(t, i, j)
                if os.path.exists(filename_pattern.format(name)):
                    dict[name] = {}
                    with open(filename_pattern.format(name)) as file:
                        # print("reading stuff")
                        lines = file.readlines()
                        for k in range(len(lines)).__reversed__():
                            # if lines[k][:10] == "makespan =" :
                            if "makespan =" in lines[k]:
                                idx_mks = lines[k].index("makespan =")
                                if 'best' not in dict[name]:
                                    dict[name]['best'] = int(lines[k][idx_mks+10:])
                                dict[name]['first'] = int(lines[k][idx_mks+10:])
                            if lines[k][:18] == "%%%mzn-stat: time=":
                                dict[name]['time'] = float(lines[k][18:])
                            # if lines[k][:19] == "%%%mzn-stat: nodes=":
                            #     node = int(lines[k][19:])
                            #     n.append(node)
                            if lines[k][:22] == "% Time limit exceeded!":
                                dict[name]['time'] = -1
                    if 'best' not in dict[name]:
                        dict[name]['best'] = math.inf
                    if 'first' not in dict[name]:
                        dict[name]['first'] = math.inf
                    if 'time' not in dict[name]:
                        dict[name]['time'] = -1

    return ResultRunSolver(caption_name, time_out, dict)


class ResultRunSolver:

    def __init__(self, name, time_out, dict):
        self.name = name
        self.time_out = time_out
        self.dict = dict
        self.nb_instance = len(dict)

    def cactus_line_time(self):
        all_times = [0] + [t for t in [self.dict[k]['time'] for k in self.dict] if t >= 0]
        all_times.sort()
        perc = [i / self.nb_instance for i in list(range(len(all_times)))]
        return all_times, perc

    def cactus_line_best(self):
        all_best = [0] + [t for t in [self.dict[k]['best'] for k in self.dict] if t >= 0]
        all_best.sort()
        perc = [i / self.nb_instance for i in list(range(len(all_best)))]
        return all_best, perc

    def cactus_line_by_bench_time_all(self):
        d = {}
        for t in PSPLIB_BENCH:
            all_times = [0] + [t for t in [self.dict[k]['time'] for k in self.dict if k.startswith(t)] if t >= 0]
            all_times.sort()
            perc = [i / (PSPLIB_BENCH_GROUP[t] * 10) for i in list(range(len(all_times)))]
            d[t] = (all_times, perc)
        return d

    def cactus_line_by_bench_time(self, subset):
        d = {}
        for t in PSPLIB_BENCH:
            all_times = [0] + [p for p in [self.dict[k]['time'] for k in subset[t] if k in self.dict] if p >= 0]
            all_times.sort()
            perc = [i / len(subset[t]) for i in list(range(len(all_times)))]
            d[t] = (all_times, perc)
        return d

    def cactus_line_by_bench_best_all(self):
        d = {}
        for t in PSPLIB_BENCH:
            for k in self.dict:
                if k.startswith(t) :
                    if 'best' not in self.dict[k]:
                        print("------------")
                        print(self.time_out)
                        print(k)
            all_times = [0] + [t for t in [self.dict[k]['best'] for k in self.dict if k.startswith(t)] if t >= 0]
            all_times.sort()
            perc = [i / (PSPLIB_BENCH_GROUP[t] * 10) for i in list(range(len(all_times)))]
            d[t] = (all_times, perc)
        return d

    def cactus_line_by_bench_best(self, subset):
        d = {}
        for t in PSPLIB_BENCH:
            for k in subset[t]:
                if k not in self.dict :
                    print("missing {}".format(k))
            all_times = [0] + [p for p in [self.dict[k]['best'] for k in subset[t] if k in self.dict] if p >= 0]
            all_times.sort()
            perc = [i / len(subset[t]) for i in list(range(len(all_times)))]
            d[t] = (all_times, perc)
        return d

    def cactus_line_by_bench_first(self):
        d = {}
        for t in PSPLIB_BENCH:
            for k in self.dict:
                if k.startswith(t) :
                    if 'first' not in self.dict[k]:
                        print("------------")
                        print(self.time_out)
                        print(k)
            all_times = [0] + [t for t in [self.dict[k]['first'] for k in self.dict if k.startswith(t)] if t >= 0]
            all_times.sort()
            perc = [i / (PSPLIB_BENCH_GROUP[t] * 10) for i in list(range(len(all_times)))]
            d[t] = (all_times, perc)
        return d
