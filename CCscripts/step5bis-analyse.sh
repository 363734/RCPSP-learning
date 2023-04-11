#! /bin/bash

generate_table_validation () {
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


  j=$(($i % 6))
  dsoptslist=(
    "TO=1000_sbps=false_vsids=false"
    "TO=60000_sbps=false_vsids=false"
    "TO=600000_sbps=false_vsids=false"
    "TO=1000_sbps=true_vsids=true"
    "TO=60000_sbps=true_vsids=true"
    "TO=600000_sbps=true_vsids=true"
  )
  dsopts=${dsoptslist[$j]}
  i=$(($i / 6))

  splitid=split1


  j=$(($i % 2))
  modellist=(
    "_bsf"
    "k"
  )
  model=${modellist[$j]}


  echo ${lr}
  echo ${dsopts}

  python ../script/tasks_graph/task_table_validation_analysis.py ${splitid} ${dsopts} ${lr} ${model}
}

for v in {0..35}
do
    generate_table_validation $v
done