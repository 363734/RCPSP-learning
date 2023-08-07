#! /bin/bash
# Train the GNN on the given datas

source ../../rcpsp/bin/activate

i=$1
echo $i


j=$(($i % 3))

lrlist=(
  0.01
  0.001
  0.0001
)
lr=${lrlist[$j]}

i=$(($i / 3))

j=$(($i % 4))

pspliblist=(
  "<=j30"
  "<=j60"
  "<=j90"
  "<=j120"
)
psplib=${pspliblist[$j]}

i=$(($i / 4))

epoch=1000

#j=$(($i % 8))
j=$(($i % 2))
dsoptslist=(
#  "TO=1000_sbps=false_vsids=false"
#  "TO=60000_sbps=false_vsids=false"
#  "TO=600000_sbps=false_vsids=false"
  "TO=3600000_sbps=false_vsids=false"
#  "TO=1000_sbps=true_vsids=true"
#  "TO=60000_sbps=true_vsids=true"
#  "TO=600000_sbps=true_vsids=true"
  "TO=3600000_sbps=true_vsids=true"
)
dsopts=${dsoptslist[$j]}
#i=$(($i / 8))
i=$(($i / 2))

j=$(($i % 10))
kcross=$j

splitid=split2

modelname=${splitid}_${kcross}_${psplib}_[${dsopts}]_${lr}

echo ${kcross}
echo ${lr}
echo ${psplib}
echo ${epoch}
echo ${dsopts}
echo ${modelname}

python ../script/tasks/task_learn_validate_predict.py --mode=learning --split-id=${splitid} --kcross=${kcross} --lr=${lr} --psplib=${psplib} --epoch=${epoch} --ds-opts=${dsopts} --model-name=${modelname} > ../target/logs_learning/log_${modelname}.txt

