#! /bin/bash
# choose the split of the benchmark (which instances are for learning, which edges are for learning)

source ../../rcpsp/bin/activate


python ../script/tasks/task_create_bench.py psplib sp

python ../script/tasks/task_create_bench.py psplib sp-u uniform "allprec_bsf_TO=1000_sbps=false_vsids=false"
python ../script/tasks/task_create_bench.py psplib sp-b balanced "allprec_bsf_TO=1000_sbps=false_vsids=false"

