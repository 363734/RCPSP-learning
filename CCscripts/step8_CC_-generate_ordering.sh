#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-0:30
#SBATCH --array=10-489#,1010-1489,2010-2489,3010-3609
#SBATCH --mem-per-cpu=1024M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

bash step8_CCarray_-generate_ordering.sh $SLURM_ARRAY_TASK_ID