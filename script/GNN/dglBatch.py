from typing import List

from script.PSPLIBinfo import BENCH_GROUP
from script.split_bench import split_bench


class Batch:
    def __init__(self, split):
        self.split = split
        self.batch = {"seen": {}, "unseen": {}, "unknown": {}, "all": {}}

    def get_batch(self, tag: str, x: List[str]):
        l = []
        for t in x:
            if t not in self.batch[tag]:
                self.batch[tag][t] = list(self.__batch_x(tag, t))
            l += self.batch[tag][t]
        return l

    def __batch_x(self, tag: str, t: str):
        if tag == "seen":
            return self.__batch_seen_x(t)
        elif tag == "unseen":
            return self.__batch_unseen_x(t)
        elif tag == "unknown":
            return self.__batch_unknown_x(t)
        elif tag == "all":
            return self.__batch_all_x(t)

    def __batch_seen_x(self, t: str):
        for i in self.split[t]["seen"]:
            for j in self.split[t][i]["seen"]:
                yield t, i, j

    def __batch_unseen_x(self, t: str):
        for i in self.split[t]["seen"]:
            for j in self.split[t][i]["unseen"]:
                yield t, i, j

    def __batch_unknown_x(self, t: str):
        for i in self.split[t]["unseen"]:
            for j in range(1, 11):
                yield t, i, j

    def __batch_all_x(self, t: str):
        for i in range(1, BENCH_GROUP[t] + 1):
            for j in range(1, 11):
                yield t, i, j


if __name__ == "__main__":
    spl = split_bench("0")
    btch = Batch(spl)
    seen30 = btch.get_batch("seen", ["j30", "j60"])
    print(seen30)
