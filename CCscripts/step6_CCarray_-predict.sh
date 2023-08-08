#! /bin/bash

source ../../rcpsp/bin/activate

model="split2_BEST_<=j120_[TO=3600000_sbps=true_vsids=true]_0.01_bsfF1"
i=$1

bi=$(($i / 1000))

benchlist=(
  "j30"
  "j60"
  "j90"
  "j120"
)

b=${benchlist[$bi]}

i=$(($i % 1000))

g=$(($i / 10))

i=$(($i % 10))

idxlist=(
  1
  2
  3
  4
  5
  6
  7
  8
  9
  10
)

idx=${idxlist[$i]}

name=${b}${g}_${idx}
echo $name

python ../script/tasks/task_learn_validate_predict.py --mode=prediction --psplib-graph=$name --model=${model} >../target/logs_prediction/log_${name}_${model}.txt
