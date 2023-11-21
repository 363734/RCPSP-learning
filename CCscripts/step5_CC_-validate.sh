#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-5:00
#SBATCH --array=0-47
#SBATCH --mem-per-cpu=5120M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

source ../../rcpsp/bin/activate

#bash step5_CCarray_-validate.sh $SLURM_ARRAY_TASK_ID

