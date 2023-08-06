#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-2:30
#SBATCH --array=0-239
#SBATCH --mem-per-cpu=5120M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

bash step4_CCarray_-trainGNN.sh $SLURM_ARRAY_TASK_ID