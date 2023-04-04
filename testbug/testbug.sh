#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-1:30
#SBATCH --mem-per-cpu=5120M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

source ../../rcpsp/bin/activate

python testbug.py