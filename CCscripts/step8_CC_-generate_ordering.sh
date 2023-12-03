#! /bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=0-0:30
#SBATCH --array=3010-3609  #10-489,1010-1489,2010-2489,3010-3609
#SBATCH --mem-per-cpu=1024M
#SBATCH --mail-user=helene.verhaeghe@polymtl.ca
#SBATCH --mail-type=ALL

source ../../rcpsp/bin/activate

a=$1
#a=$SLURM_ARRAY_TASK_ID

#model="sp_sp-b_BEST_<=j30_[allprec_bsf_TO=1000_sbps=false_vsids=false]_0.01_bsfLoss"
model="sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=true_vsids=true]_0.01_bsfLoss"
#model="sp_sp-u_BEST_<=j120_[allprec_bsf_TO=3600000_sbps=false_vsids=false]_0.01_bsfLoss"

threshold=0.75

datadir="../target/datas"

i=0
for b in "j30" "j60" "j90" "j120"
do
  j=$i
  for g in {0..60}
  do
    for idx in {1..10}
    do
      if (( $j == $a )) ; then
          name=${b}${g}_${idx}
          echo ${name}

          instance_file="../target/datas/psplib/${b}/${name}.sm"
          precedence_file="../target/prediction/${model}/prec_${name}_${threshold}_[${model}].txt"
          ordering_file="../target/prediction/${model}/orde_${name}_${threshold}_[${model}].txt"
          log_dir="../target/logs_ordering/${model}"
          log_file="${log_dir}/log_orde_${name}_${threshold}_[${model}].txt"
          mkdir -p ${log_dir}
          echo ${precedence_file}
          echo ${ordering_file}


if [ -f "${instance_file}" ]; then
    echo "${instance_file} exists."
else
    echo "${instance_file} does not exist."
fi
if [ -f "${precedence_file}" ]; then
    echo "${precedence_file} exists."
else
    echo "${precedence_file} does not exist."
fi

          ../chuffed/rcpsp-ordering ${instance_file} :add_prec ${precedence_file} :print_ordering ${ordering_file} > ${log_file}
      fi
      j=$((j+1))
    done
  done
  i=$((i+1000))
done