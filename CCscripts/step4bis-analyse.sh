#! /bin/bash

splitid1=sp
#splitid2=sp-b
splitid2=sp-u

outdir=../target/results_graphs/learning_${splitid1}_${splitid2}
mkdir -p ${outdir}

for lr in 0.01 0.001 0.0001
do
  for psplib in "<=j30" "<=j60" "<=j90" "<=j120"
  do
    for T in  1000 60000 600000 3600000
    do
      for opt in "sbps=false_vsids=false" "sbps=true_vsids=true"
      do
        dsopts="allprec_bsf_TO=${T}_${opt}"
        for kcross in {0..9}
        do
          modelname=${splitid1}_${splitid2}_${kcross}_${psplib}_[${dsopts}]_${lr}

          echo ${lr}
          echo ${psplib}
          echo ${dsopts}
          echo ${kcross}
          echo ${modelname}

          logfile=../target/logs_learning/log_${modelname}.txt
          graphfile=${outdir}/learning_${modelname}.pdf

          python ../script/tasks_graph/task_graph_learning_analysis.py ${logfile} ${graphfile}

        done
      done
    done
  done
done


