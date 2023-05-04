#! /bin/bash


source ../../rcpsp/bin/activate

model="split2_20-80_<=j120_[TO=3600000_sbps=true_vsids=true]_0.001_bsf"
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

log_dir="../target/run_local_search/${model}"
mkdir -p ${log_dir}


tototal=3600000
#tototal=900000

# test 1: sbps only, short timeout of round
toround=2000
vsids="false"
sbps="false"
lskeep=0.3

outfile="ls_${name}_${threshold}_[${model}]_${lskeep}_TO=${toround}-${tototal}_sbps=${sbps}_vsids=${vsids}.txt"

python ../script/tasks/task_simulated_local_search.py --psplib-graph=${name} --model-name=${model} --threshold=${threshold} --to-total=${tototal} --to-round=${toround} --vsids=${vsids} --sbps=${sbps} --ls-keep=${lskeep} > ${log_dir}/${outfile}



## test 2: sbps+vsids
#toround=120000
#vsids="true"
#sbps="true"
#
#
#outfile="ls_${name}_${threshold}_[${model}]_${lskeep}_TO=${toround}-${tototal}_sbps=${sbps}_vsids=${vsids}.txt"
#
#python ../script/tasks/task_simulated_local_search.py --psplib-graph=${name} --model-name=${model} --threshold=${threshold} --to-total=${tototal} --to-round=${toround} --vsids=${vsids} --sbps=${sbps} --ls-keep=${lskeep} > ${log_dir}/${outfile}
#
#
