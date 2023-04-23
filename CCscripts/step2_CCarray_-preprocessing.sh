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

#python ../script/tasks/task_preprocess_instance.py $b $g $idx
python ../script/tasks/task_preload_data_graph.py $b $g $idx


