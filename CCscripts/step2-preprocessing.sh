#! /bin/bash
# Preprocess the file (generate the instances and solve them the given number of time)

datadir="../target/datas"
preprocessdir="../target/preprocessed"

for b in "j30" "j60" "j90" "j120"; do

  mkdir -p $preprocessdir/$b

  for f in $datadir/$b/*; do

    bn="$(basename -- $f)"
    bn="${bn%.*}"
    id="${bn#*_}"
    bn="${bn%_*}"
    bn="${bn#${b}}"

    python ../script/tasks/task_preprocess_instance.py $b $bn $i

  done
done

python ../script/tasks/task_aggerate_bounds.py
