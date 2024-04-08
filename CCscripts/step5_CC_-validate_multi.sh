#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-2:00
#SBATCH --array=0-95
#SBATCH --mem-per-cpu=5120M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

source ../../rcpsp/bin/activate

#bash step5_CCarray_-validate.sh $SLURM_ARRAY_TASK_ID


#a=$1
a=$SLURM_ARRAY_TASK_ID

splitid1=sp
#splitid2=sp-u
splitid2=sp-b

epoch=1000

j=0
for lr in 0.01 0.001 0.0001
do
  for psplib in "<=j30" "<=j60"
  do
    for T in  600000
    do
      for opt in "sbps=false_vsids=false" "sbps=true_vsids=true"
      do
        for perc in 0.5 0.7
        do
          dsopts="allprec_bsf_ubto=3600000_TO=${T}_${opt}_p=${perc}"
          modelname=${splitid1}_${splitid2}_BEST_${psplib}_[${dsopts}]_${lr}_bsfLoss
          for psplibeval in "j30" "j60" "j90" "j120"
          do
            if (( $j == $a )) ; then
              for subbatch in "unseen" "unknown" "all" "seen"
              do
                echo ${lr}
                echo ${psplib}
                echo ${epoch}
                echo ${dsopts}
                echo ${modelname}

                python ../script/tasks/task_learn_validate_predict.py --mode=evaluation --formatting=psplib --split-id=${splitid1} --split-cross-id=${splitid2} --psplib=${psplibeval} --subbatch=${subbatch} --ds-opts=${dsopts} --model-name=${modelname} --multi> ../target/logs_validation/log_${modelname}_${psplibeval}_${subbatch}.txt

              done

            fi
            j=$((j+1))
          done
        done
      done
    done
  done
done

