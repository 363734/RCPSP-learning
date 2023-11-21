#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-3:00
#SBATCH --array=0-7
#SBATCH --mem-per-cpu=5120M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

# choose the split of the benchmark (which instances are for learning, which edges are for learning)

source ../../rcpsp/bin/activate


#python ../script/tasks/task_create_bench.py psplib sp

a=$SLURM_ARRAY_TASK_ID

j=0
for T in  1000 60000 600000 3600000
do
  for opt in "sbps=false_vsids=false" "sbps=true_vsids=true"
  do
    if (( $j == $a )) ; then
      dataset="allprec_bsf_TO=${T}_${opt}"
      python ../script/tasks/task_create_bench.py psplib sp-u uniform ${dataset}
      python ../script/tasks/task_create_bench.py psplib sp-b balanced ${dataset}

    fi
    j=$((j+1))
  done
done

