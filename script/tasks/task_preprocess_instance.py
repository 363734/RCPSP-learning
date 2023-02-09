import sys

from script.tasks import generate_all_for_one

if __name__ == "__main__":
    assert len(sys.argv) == 4
    bench = sys.argv[1]
    bench_group = int(sys.argv[2])
    instance_id = int(sys.argv[3])
    name = "{}{}_{}".format(bench, bench_group, instance_id)

    generate_all_for_one(bench, name, [1000, 60000, 600000])
