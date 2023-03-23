#! /bin/bash
# Download data from PSPLIB

source ../../rcpsp/bin/activate

#setup the structure of the project
python ../script/tasks/task_create_structure_of_project.py

#download datas
datadir="../target/datas"

for b in "j30" "j60" "j90" "j120"; do

  mkdir -p $datadir/$b

  wget -O $datadir/$b/$b.zip https://www.om-db.wi.tum.de/psplib/files/$b.sm.zip
  unzip $datadir/$b/$b.zip -d $datadir/$b/
  rm $datadir/$b/$b.zip

  hrsfile=$datadir/${b}hrs.sm
  wget -O $hrsfile https://www.om-db.wi.tum.de/psplib/files/${b}hrs.sm
  iconv -f utf-8 -t utf-8 -c $hrsfile -o $hrsfile

  if [ $b == "j30" ]; then
    optfile=$datadir/${b}opt.sm
    wget -O $optfile https://www.om-db.wi.tum.de/psplib/files/${b}opt.sm
    iconv -f utf-8 -t utf-8 -c $optfile -o $optfile
  else
    lbfile=$datadir/${b}lb.sm
    wget -O $lbfile https://www.om-db.wi.tum.de/psplib/files/${b}lb.sm
    iconv -f utf-8 -t utf-8 -c $lbfile -o $lbfile
  fi

done

python ../script/tasks/task_aggerate_bounds.py
