#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-4:00
#SBATCH --array=0-959
#SBATCH --mem-per-cpu=5120M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

source ../../rcpsp/bin/activate


#a=$1
a=$SLURM_ARRAY_TASK_ID

splitid1=sp
#splitid2=sp-b
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
        for kcross in {0..9}
        do
          if (( $j == $a )) ; then
            modelname=${splitid1}_${splitid2}_${kcross}_${psplib}_[${dsopts}]_${lr}

            echo ${lr}
            echo ${psplib}
            echo ${epoch}
            echo ${dsopts}
            echo ${kcross}
            echo ${modelname}

            python ../script/tasks/task_learn_validate_predict.py --mode=learning --split-id=${splitid1} --split-cross-id=${splitid2} --kcross=${kcross} --lr=${lr} --psplib=${psplib} --epoch=${epoch} --ds-opts=${dsopts} --model-name=${modelname} > ../target/logs_learning/log_${modelname}.txt

          fi
          j=$((j+1))
        done
      done
    done
  done
done