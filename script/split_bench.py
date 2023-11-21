import os
from script.Instances.bench import mapfctformat
from script.logs import step_log
from script.parameters import DIR_SPLIT
from script.save_pickle_json import j_save, j_load

SUBSPLIT = ["seen", "unseen", "unknown", "all"]


def split_bench(formatting: str, tag: str):
    name = "split_{}.json".format(tag)
    dir_name = os.path.join(DIR_SPLIT, formatting)
    filename = os.path.join(dir_name, name)
    if os.path.exists(filename):
        step_log("Load from existing split (format: {}, split: {})".format(formatting, tag))
        return j_load(filename)
    else:
        step_log("Creating new split (format: {}, split: {})".format(formatting, tag))
        os.makedirs(dir_name, exist_ok=True)
        bench = {"format": formatting, "tag": tag}
        bench = mapfctformat[formatting]["split_bench"](bench)
        j_save(filename, bench)
        return bench



# def split_instance_cross(formatting: str, tag: str, inst: RCPSP, prec_file: str):
#     param_tag = os.path.basename(prec_file)
#     bench = 42#from_bench(param_tag)
#     name = "split_{}_{}.json".format(tag, param_tag)
#     dir_name = os.path.join(DIR_SPLIT, formatting, tag, bench)
#     filename = os.path.join(dir_name, name)
#     if os.path.exists(filename):
#         print("Load from existing split")
#         return j_load(filename)
#     else:
#         os.makedirs(dir_name, exist_ok=True)
#         precedences = filter_precedence(inst, parse_precedence(prec_file)) # prec file from solution constains transitive closure already
#         return split_single_instance(inst, precedences, filename, u_or_b)

def split_extract_cross(kcross:int, cross_split):
    test = cross_split[kcross]
    train = cross_split[:kcross] + cross_split[kcross+1:]
    return train, test

# if __name__ == "__main__":
#     # print(split_bench("0"))
#     inst = parse_rcpsp(os.path.join(DIR_DATAS, "psplib/j30/j301_1.sm"))
#     a = split_instance_cross("0", inst,
#                              os.path.join(DIR_DATA_PREPROCESSED, "psplib/j30/j301_1_all_prec_optimal_solution_TO=1000_sbps=OFF.txt"))
#     print(a)
