#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-5:00
#SBATCH --mem-per-cpu=7000M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

source ../../rcpsp/bin/activate


#model="sp_sp-b_0_<=j30_[allprec_bsf_TO=60000_sbps=false_vsids=false]_0.01_bsfLoss"
#model="sp_sp-u_BEST_<=j60_[allprec_bsf_TO=3600000_sbps=true_vsids=true]_0.01_bsfLoss"
#model="sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=true_vsids=true]_0.01_bsfLoss"
#model="sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=false_vsids=false]_0.01_bsfLoss"


model="sp_sp-u_BEST_<=j60_[allprec_bsf_ubto=3600000_TO=600000_sbps=true_vsids=true_p=0.7]_0.01_bsfLoss"

threshold=0.99
#threshold=0.95
#threshold=0.75
#threshold=0.55
#threshold=0.5

splittag="sp"

outputfile="stat_[${model}]_${threshold}.txt"


python ../script/tasks_graph/task_graph_run_analysis.py ${model} ${threshold} ${splittag}
python ../script/tasks_graph/task_stats_run_analysis.py ${model} ${threshold} ${outputfile}



