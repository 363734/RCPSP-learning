#! /bin/bash

source ../../rcpsp/bin/activate

model="split2_20-80_<=j120_[TO=600000_sbps=true_vsids=true]_0.001_bsf"
threshold=0.55

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

prediction_file="../target/prediction/${model}/pred_${name}_[${model}].txt"

python ../script/tasks/task_filter_prediction.py ${prediction_file} ${threshold}


