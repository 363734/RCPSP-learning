#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-1:30
#SBATCH --array=10-489,1010-1489  #10-489,1010-1489,2010-2489,3010-3609
#SBATCH --mem-per-cpu=1024M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

source ../../rcpsp/bin/activate

#a=$1
a=$SLURM_ARRAY_TASK_ID

solver=chuffed
#solver=cpmpyortools # TODO
nbsol=100
toub=3600000 #timeout ub value

i=0
for BENCH in "j30" "j60" "j90" "j120"
do
  j=$i
  for G in {0..60}
  do
    for IDX in {1..10}
    do
      if (( $j == $a )) ; then
        for T in 600000
        do
          #python ../script/tasks/task_preprocess_instance_multisol.py psplib $BENCH $G $IDX $solver $toub $T $nbsol
          for P in 0.7 0.5
          do
            python ../script/tasks/task_aggregate_multisol.py psplib $BENCH $G $IDX "ubto=3600000_TO=600000_sbps=false_vsids=false" $P "TO=600000_sbps=false_vsids=false"
            python ../script/tasks/task_aggregate_multisol.py psplib $BENCH $G $IDX "ubto=3600000_TO=600000_sbps=true_vsids=true" $P "TO=600000_sbps=true_vsids=true"
          done
        done
      fi
      j=$((j+1))
    done
  done
  i=$((i+1000))
done

