import os

from scripts.Instances.upperbound import read_opt, read_hrs, read_lb, save_bounds
from scripts.PSPLIBinfo import BENCH
from scripts.parameters import DIR_PREPROCESSED, DIR_DATAS


# aggregate the bounds from the 3 types of bound file available on the PSPLib website
# write the aggregated bounds within a single file
def aggregate_bounds():
    best_dict = {}
    for b in BENCH:
        if b == 'j30':
            read_opt(os.path.join(DIR_DATAS, "{}opt.sm".format(b)), b, best_dict)
            read_hrs(os.path.join(DIR_DATAS, "{}hrs.sm".format(b)), b, best_dict)
        else:
            read_hrs(os.path.join(DIR_DATAS, "{}hrs.sm".format(b)), b, best_dict)
            read_lb(os.path.join(DIR_DATAS, "{}lb.sm".format(b)), b, best_dict)
    save_bounds(os.path.join(DIR_PREPROCESSED, "bounds.txt"), best_dict)


if __name__ == "__main__":
    aggregate_bounds()
