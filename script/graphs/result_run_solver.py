import os

from script.PSPLIBinfo import BENCH, BENCH_GROUP


class ResultRunSolver:

    def __init__(self, filename_pattern: str, name: str, time_out:int):
        self.name = name
        self.time_out = time_out
        self.dict = {}
        for t in BENCH:
            for i in range(1, BENCH_GROUP[t] + 1):
                for j in range(1, 11):
                    print("Read results for {}".format(filename_pattern.format(t, name)))
                    name = "{}{}_{}".format(t, i, j)
                    if os.path.exists(filename_pattern.format(t, name)):
                        self.dict[name] = {}
                        with open(filename_pattern.format(t, name)) as file:
                            # print("reading stuff")
                            lines = file.readlines()
                            for k in range(len(lines)).__reversed__():
                                if lines[k][:10] == "makespan =" and 'best' not in self.dict[name]:
                                    self.dict[name]['best'] = int(lines[k][10:])
                                if lines[k][:18] == "%%%mzn-stat: time=":
                                    self.dict[name]['time'] = float(lines[k][18:])
                                # if lines[k][:19] == "%%%mzn-stat: nodes=":
                                #     node = int(lines[k][19:])
                                #     n.append(node)
                                if lines[k][:22] == "% Time limit exceeded!":
                                    self.dict[name]['time'] = -1

        self.nb_instance = len(self.dict)

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
            perc = [i / (BENCH_GROUP[t]*10) for i in list(range(len(all_times)))]
            d[t] = (all_times, perc)
        return d

    def cactus_line_by_bench_best(self):
        d = {}
        for t in BENCH:
            all_times = [0] + [t for t in [self.dict[k]['best'] for k in self.dict if k.startswith(t)] if t >= 0]
            all_times.sort()
            perc = [i / (BENCH_GROUP[t]*10) for i in list(range(len(all_times)))]
            d[t] = (all_times, perc)
        return d
