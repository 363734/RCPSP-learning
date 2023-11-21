# file with logging methods


def step_log(l: str):
    print("     :-: {}".format(l))


def title_log(l: str):
    print(":-: {}".format(l))


def warning_log(l: str):
    print(":!!: {}".format(l))


def error_log(l: str):
    print(":ERR: {}".format(l))
    exit(1)
