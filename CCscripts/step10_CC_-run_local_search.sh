#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-2:30
#SBATCH --array=10-489# 10-489,1010-1489,2010-2489,3010-3609
#SBATCH --mem-per-cpu=1024M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

bash step10_CCarray_-run_local_search.sh $SLURM_ARRAY_TASK_ID