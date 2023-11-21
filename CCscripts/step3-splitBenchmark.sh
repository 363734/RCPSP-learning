#! /bin/bash
# choose the split of the benchmark (which instances are for learning, which edges are for learning)

source ../../rcpsp/bin/activate


python ../script/tasks/task_create_bench.py psplib sp

for T in  1000 60000 600000 3600000
do
  for opt in "sbps=false_vsids=false" "sbps=true_vsids=true"
  do

    dataset="allprec_bsf_TO=${T}_${opt}"
    python ../script/tasks/task_create_bench.py psplib sp-u uniform ${dataset}
    python ../script/tasks/task_create_bench.py psplib sp-b balanced ${dataset}

  done
done

