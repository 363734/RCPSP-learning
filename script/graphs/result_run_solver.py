import math
import os

from script.PSPLIBinfo import BENCH, BENCH_GROUP


def parse_preprocessed_result(filename_pattern: str, caption_name: str, time_out: int):
    dict = {}
    for t in BENCH:
        for i in range(1, BENCH_GROUP[t] + 1):
            for j in range(1, 11):
                print("Read results for {}".format(filename_pattern.format(t, caption_name)))
                name = "{}{}_{}".format(t, i, j)
                if os.path.exists(filename_pattern.format(t, name)):
                    dict[name] = {}
                    with open(filename_pattern.format(t, name)) as file:
                        # print("reading stuff")
                        lines = file.readlines()
                        for k in range(len(lines)).__reversed__():
                            if lines[k][:10] == "makespan =" and 'best' not in dict[name]:
                                dict[name]['best'] = int(lines[k][10:])
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
    for t in BENCH:
        for i in range(1, BENCH_GROUP[t] + 1):
            for j in range(1, 11):
                print("Read results for {}".format(filename_pattern.format(caption_name)))
                name = "{}{}_{}".format(t, i, j)
                if os.path.exists(filename_pattern.format(name)):
                    dict[name] = {}
                    with open(filename_pattern.format(name)) as file:
                        # print("reading stuff")
                        lines = file.readlines()
                        for k in range(len(lines)).__reversed__():
                            if lines[k][:10] == "makespan =" and 'best' not in dict[name]:
                                dict[name]['best'] = int(lines[k][10:])
                            if lines[k][:18] == "%%%mzn-stat: time=":
                                dict[name]['time'] = float(lines[k][18:])
                            # if lines[k][:19] == "%%%mzn-stat: nodes=":
                            #     node = int(lines[k][19:])
                            #     n.append(node)
                            if lines[k][:22] == "% Time limit exceeded!":
                                dict[name]['time'] = -1
                    if 'best' not in dict[name]:
                        dict[name]['best'] = math.inf
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

    def cactus_line_by_bench_time(self):
        d = {}
        for t in BENCH:
            all_times = [0] + [t for t in [self.dict[k]['time'] for k in self.dict if k.startswith(t)] if t >= 0]
            all_times.sort()
            perc = [i / (BENCH_GROUP[t] * 10) for i in list(range(len(all_times)))]
            d[t] = (all_times, perc)
        return d

    def cactus_line_by_bench_best(self):
        d = {}
        for t in BENCH:
            for k in self.dict:
                if k.startswith(t) :
                    if 'best' not in self.dict[k]:
                        print("------------")
                        print(self.time_out)
                        print(k)
            all_times = [0] + [t for t in [self.dict[k]['best'] for k in self.dict if k.startswith(t)] if t >= 0]
            all_times.sort()
            perc = [i / (BENCH_GROUP[t] * 10) for i in list(range(len(all_times)))]
            d[t] = (all_times, perc)
        return d
