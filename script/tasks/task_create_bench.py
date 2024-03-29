import os
import sys

from script.Instances.bench import mapfctformat
# from script.Instances.bench import mapfctformat

from script.logs import title_log
from script.parameters import DIR_SPLIT, DIR

from script.split_bench import split_bench

if __name__ == "__main__":
    formatting = sys.argv[1]
    tag = sys.argv[2]
    if len(sys.argv) == 3:
        split_bench(formatting, tag)
    elif len(sys.argv) > 3:
        s_or_m = sys.argv[3]
        u_or_b = sys.argv[4]  # uniform or balanced
        precfileopt = sys.argv[5]
        title_log("Creating split tag={} for bench {} with options [{}]".format(tag, formatting, precfileopt))
        dir_name = os.path.join(DIR[s_or_m]['SPLIT'], formatting, tag)
        os.makedirs(dir_name, exist_ok=True)
        mapfctformat[formatting]["split_instances_cross"](tag, precfileopt, u_or_b, s_or_m)
