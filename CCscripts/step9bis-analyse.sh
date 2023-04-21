#! /bin/bash


source ../../rcpsp/bin/activate

#model="split1_50-50_<=j120_[TO=600000_sbps=false_vsids=false]_0.001_bsf"
model="split1_20-80_<=j120_[TO=600000_sbps=true_vsids=true]_0.001_bsf"
#model="split1_20-80_<=j90_[TO=600000_sbps=true_vsids=true]_0.001_bsf"
#threshold=0.75
threshold=0.55
splittag=split1

python ../script/tasks_graph/task_graph_run_analysis.py ${model} ${threshold} ${splittag}

