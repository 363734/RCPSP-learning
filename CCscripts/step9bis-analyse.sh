#! /bin/bash


source ../../rcpsp/bin/activate


#model="sp_sp-b_0_<=j30_[allprec_bsf_TO=60000_sbps=false_vsids=false]_0.01_bsfLoss"
#model="sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=true_vsids=true]_0.01_bsfLoss"
model="sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=false_vsids=false]_0.01_bsfLoss"

#threshold=0.75
threshold=0.55
splittag=sp

python ../script/tasks_graph/task_graph_run_analysis.py ${model} ${threshold} ${splittag}
#python ../script/tasks_graph/task_stats_run_analysis.py ${model} ${threshold} ${splittag}



