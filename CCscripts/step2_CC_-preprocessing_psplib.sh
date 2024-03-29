#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-1:30
#SBATCH --array=10-489  #10-489,1010-1489,2010-2489,3010-3609
#SBATCH --mem-per-cpu=1024M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

source ../../rcpsp/bin/activate

#a=$1
a=$SLURM_ARRAY_TASK_ID

solver=chuffed
#solver=cpmpyortools # TODO

i=0
for BENCH in "j30" "j60" "j90" "j120"
do
  j=$i
  for G in {0..60}
  do
    for IDX in {1..10}
    do
      if (( $j == $a )) ; then
        python ../script/tasks/task_preload_data_graph.py psplib $BENCH $G $IDX
        for T in 1000 60000 600000 3600000
        do
          python ../script/tasks/task_preprocess_instance.py psplib $BENCH $G $IDX $solver $T
        done
      fi
      j=$((j+1))
    done
  done
  i=$((i+1000))
done

