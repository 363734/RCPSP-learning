BENCH = ["j30", "j60", "j90", "j120"]
BENCH_GROUP = {"j30": 48, "j60": 48, "j90": 48, "j120": 60}


def from_bench(name: str):
    for b in BENCH:
        if b in name:
            return b


def parse_bench_psplib(s: str):
    if s[:2] == "<=":
        return BENCH[:BENCH.index(s[2:])+1]
    elif s[:2] == ">=":
        return BENCH[BENCH.index(s[2:]):]
    elif s in BENCH:
        return [s]
    else:
        print("PSPLIB benchmarck not well defined")
        print("use the name of one bench such as 'j60'")
        print("or '<=j60' to define all that are smaller too")
        print("or '>=j60' to define all that are greater too")
        exit(1)
