#! /bin/bash

source ../../rcpsp/bin/activate

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

name=$b$g_$idx
echo $name


python ../script/tasks/task_learn_validate_predict.py --mode=prediction --psplib-graph=$name --model="split1_50-50_<=j120_[TO=600000_sbps=false_vsids=false]_0.001_bsf"
