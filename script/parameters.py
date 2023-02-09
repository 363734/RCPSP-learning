config = {
    "configNaif": {
        "solver": "rcpsp-psplib",
        "addopt": ":naif",
        "tag": "naif"
    },
    "config1": {
        "solver": "rcpsp-psplib",
        "addopt": ":ttef :sbps",
        "tag": "TS"
    }
}

USED_CONFIG = "config1"

SOLVER = config[USED_CONFIG]["solver"]
ADDOPT = config[USED_CONFIG]["addopt"]
TAG = config[USED_CONFIG]["tag"]
