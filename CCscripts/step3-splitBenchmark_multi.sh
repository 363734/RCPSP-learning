#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-3:00
#SBATCH --array=0-3
#SBATCH --mem-per-cpu=5120M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

# choose the split of the benchmark (which instances are for learning, which edges are for learning)

source ../../rcpsp/bin/activate


python ../script/tasks/task_create_bench.py psplib sp

#a=$1
a=$SLURM_ARRAY_TASK_ID

j=0
for T in 600000
do
  for opt in "sbps=false_vsids=false" "sbps=true_vsids=true"
  do
    for perc in 0.5 0.7
    do
      if (( $j == $a )) ; then
        dataset="allprec_bsf_ubto=3600000_TO=${T}_${opt}_p=${perc}"
        python ../script/tasks/task_create_bench.py psplib sp-u multi uniform ${dataset}
        python ../script/tasks/task_create_bench.py psplib sp-b multi balanced ${dataset}

      fi
      j=$((j+1))
    done
  done
done

