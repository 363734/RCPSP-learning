#! /bin/bash


splitid1=sp
splitid2=sp-u
#splitid2=sp-b

epoch=1000

j=0
for lr in 0.01 0.001 0.0001
do
  for T in  1000 60000 600000 3600000
  do
    for opt in "sbps=false_vsids=false" "sbps=true_vsids=true"
    do
      dsopts="allprec_bsf_TO=${T}_${opt}"
      model="_bsfLoss"
      echo ${lr}
      echo ${dsopts}

      python ../script/tasks_graph/task_table_validation_analysis.py ${splitid1} ${splitid2} ${dsopts} ${lr} ${model}

    done
  done
done
