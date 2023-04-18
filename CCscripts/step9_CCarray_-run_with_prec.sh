#! /bin/bash

source ../../rcpsp/bin/activate

model="split1_20-80_<=j90_[TO=600000_sbps=true_vsids=true]_0.001_bsf"
threshold=0.75

datadir="../target/datas"

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



log_dir="../target/run_result/${model}"
mkdir -p ${log_dir}


python ../script/tasks/task_run_with_prec.py ${b} ${g} ${idx} ${model} ${threshold}
