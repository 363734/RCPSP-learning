#! /bin/bash


generate_graph () {
  i=$1
  echo $i

  j=$(($i % 3))

  ttlist=(
    "80-20"
    "50-50"
    "20-80"
  )
  tt=${ttlist[$j]}

  i=$(($i / 3))

  j=$(($i % 3))

  lrlist=(
    0.01
    0.001
    0.0001
  )
  lr=${lrlist[$j]}

  i=$(($i / 3))

  j=$(($i % 3)) #TODO

  pspliblist=(
    "<=j30"
    "<=j60"
    "<=j90"
    #"<=j120" TODO
  )
  psplib=${pspliblist[$j]}

  i=$(($i / 3)) #TODO

  epoch=1000

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

  splitid=split1

  modelname=${splitid}_${tt}_${psplib}_[${dsopts}]_${lr}

  echo ${tt}
  echo ${lr}
  echo ${psplib}
  echo ${epoch}
  echo ${dsopts}

  echo ${modelname}
  logfile=../target/logs_learning/log_${modelname}.txt
  graphfile=../target/results_graphs/learning_${modelname}.pdf

  python ../script/tasks_graph/task_graph_learning_analysis.py ${logfile} ${graphfile}

}

for v in {0..215}
do
    generate_graph $v
done