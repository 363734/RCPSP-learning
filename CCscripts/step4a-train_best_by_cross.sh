#! /bin/bash
# for each the 10 cross cut, find best

source ../../rcpsp/bin/activate

for a in {0..23}
do
#a=$1
#a=$SLURM_ARRAY_TASK_ID

splitid1=sp
splitid2=sp-u

epoch=1000

j=0
for lr in 0.01 0.001 0.0001
do
  for psplib in "<=j30" "<=j60" "<=j90" "<=j120"
  do
    for T in  1000 60000 600000 3600000
    do
      for opt in "sbps=false_vsids=false" "sbps=true_vsids=true"
      do
        dsopts="allprec_bsf_TO=${T}_${opt}"

        if (( $j == $a )) ; then

          modelnamepatternLoss=${splitid1}_${splitid2}_{}_${psplib}_[${dsopts}]_${lr}_bsfLoss

          echo ${lr}
          echo ${psplib}
          echo ${epoch}
          echo ${dsopts}
          echo ${modelnamepatternLoss}

          python ../script/tasks/task_best_cross.py ${modelnamepatternLoss}

        fi
        j=$((j+1))

      done
    done
  done
done

done
