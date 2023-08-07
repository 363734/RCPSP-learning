#! /bin/bash
# for each the 10 cross cut, find best

source ../../rcpsp/bin/activate

for i in {0..23}; do

#  i=$1
#  echo $i

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


  splitid=split2

  modelnamepatternF1=${splitid}_{}_${psplib}_[${dsopts}]_${lr}_bsfF1
  modelnamepatternPREC=${splitid}_{}_${psplib}_[${dsopts}]_${lr}_bsfPREC

  echo ${lr}
  echo ${psplib}
  echo ${dsopts}
  echo ${modelnamepatternF1}
  echo ${modelnamepatternPREC}

  python ../script/tasks/task_best_cross.py ${modelnamepatternF1}
  python ../script/tasks/task_best_cross.py ${modelnamepatternPREC}

done
