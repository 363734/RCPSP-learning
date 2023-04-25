#! /bin/bash

source ../../rcpsp/bin/activate

generate_validation () {
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

#  j=$(($i % 8))
#  dsoptslist=(
#    "TO=1000_sbps=false_vsids=false"
#    "TO=60000_sbps=false_vsids=false"
#    "TO=600000_sbps=false_vsids=false"
#    "TO=3600000_sbps=false_vsids=false"
#    "TO=1000_sbps=true_vsids=true"
#    "TO=60000_sbps=true_vsids=true"
#    "TO=600000_sbps=true_vsids=true"
#    "TO=3600000_sbps=true_vsids=true"
#  )
#  dsopts=${dsoptslist[$j]}
#  i=$(($i / 8))

  j=$(($i % 2))
  dsoptslist=(
    "TO=3600000_sbps=false_vsids=false"
    "TO=3600000_sbps=true_vsids=true"
  )
  dsopts=${dsoptslist[$j]}
  i=$(($i / 2))

  splitid=split2

  modelname=${splitid}_${tt}_${psplib}_[${dsopts}]_${lr}



  j=$(($i % 4))
  psplibevallist=(
    "j120"
    "j90"
    "j60"
    "j30"
  )
  psplibeval=${psplibevallist[$j]}
  i=$(($i / 4))

  j=$(($i % 4))
  subbatchlist=(
    "unseen"
    "unknown"
    "all"
    "seen"
  )
  subbatch=${subbatchlist[$j]}
  i=$(($i / 4))

  j=$(($i % 2))
  modellist=(
    "_bsf"
    ""
  )
  model=${modellist[$j]}

  modelname=${modelname}${model}

  echo ${tt}
  echo ${lr}
  echo ${psplib}
  echo ${epoch}
  echo ${dsopts}
  echo ${psplibeval}
  echo ${subbatch}
  echo ${modelname}

  python ../script/tasks/task_learn_validate_predict.py --mode=evaluation --split-id=${splitid} --psplib=${psplibeval} --subbatch=${subbatch} --ds-opts=${dsopts} --model-name=${modelname} > ../target/logs_validation/log_${modelname}_${psplibeval}_${subbatch}.txt
}

g=$1
for v in {0..15}
do
    h=$(($g * 16))
    k=$(($h + $v))
    generate_validation $k
done
