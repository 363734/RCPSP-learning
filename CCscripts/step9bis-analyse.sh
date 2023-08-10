#! /bin/bash


source ../../rcpsp/bin/activate

model="split2_BEST_<=j120_[TO=3600000_sbps=true_vsids=true]_0.01_bsfF1"
#model="split2_BEST_<=j120_[TO=3600000_sbps=false_vsids=false]_0.01_bsfF1"

#threshold=0.75
threshold=0.55
splittag=split2

#python ../script/tasks_graph/task_graph_run_analysis.py ${model} ${threshold} ${splittag}
python ../script/tasks_graph/task_stats_run_analysis.py ${model} ${threshold} ${splittag}



