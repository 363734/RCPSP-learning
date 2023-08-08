#! /bin/bash

source ../../rcpsp/bin/activate

model="split2_BEST_<=j120_[TO=3600000_sbps=true_vsids=true]_0.01_bsfF1"
threshold=0.55

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


instance_file="../target/datas/${b}/${name}.sm"
precedence_file="../target/prediction/${model}/prec_${name}_${threshold}_[${model}].txt"
ordering_file="../target/prediction/${model}/orde_${name}_${threshold}_[${model}].txt"
log_dir="../target/logs_ordering/${model}"
log_file="${log_dir}/log_orde_${name}_${threshold}_[${model}].txt$"
mkdir -p ${log_dir}
echo ${precedence_file}
echo ${ordering_file}


../chuffed/rcpsp-ordering ${instance_file} :add_prec ${precedence_file} :print_ordering ${ordering_file} > ${log_file}

