import sys

from script.Instances.benchPSPLIB import PSPLIB, aggregate_bounds_psplib
from script.logs import *


# aggregate the bounds from the 3 types of bound file available on the PSPLib website
# write the aggregated bounds within a single file
def aggregate_bounds(formatting: str = PSPLIB):
    if formatting == PSPLIB:
        aggregate_bounds_psplib()
    else:  # TODO add new dataset here
        warning_log("Format {} is not supported for the RCPSP instance".format(formatting))


if __name__ == "__main__":
    aggregate_bounds(sys.argv[1])
