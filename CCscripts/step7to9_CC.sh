#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-8:00
#SBATCH --array=3010-3609  #10-489,1010-1489,2010-2489,3010-3609
#SBATCH --mem-per-cpu=5120M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

bash step7_CC_-filter_prediction.sh $SLURM_ARRAY_TASK_ID

bash step8_CC_-generate_ordering.sh $SLURM_ARRAY_TASK_ID

bash step9_CC_-run_with_prec.sh $SLURM_ARRAY_TASK_ID

