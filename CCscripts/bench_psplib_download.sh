#! /bin/bash
# Download data from PSPLIB

source ../../rcpsp/bin/activate

datadir="../target/datas"
psplibdir="${datadir}/psplib"

mkdir -p $psplibdir

echo ":-: Download of PSPLIB data"
for b in "j30" "j60" "j90" "j120"; do
  echo ":-: Download of PSPLIB data: benchmark $b"

  mkdir -p $datadir/$b

  wget -O $datadir/$b/$b.zip https://www.om-db.wi.tum.de/psplib/files/$b.sm.zip
  unzip $datadir/$b/$b.zip -d $datadir/$b/
  rm $datadir/$b/$b.zip

  hrsfile=$datadir/${b}hrs.sm
  hrsfiletmp=$datadir/${b}hrstmp.sm
  wget -O $hrsfiletmp https://www.om-db.wi.tum.de/psplib/files/${b}hrs.sm
  iconv -f utf-8 -t utf-8 -c $hrsfiletmp > $hrsfile
  rm $hrsfiletmp

  if [ $b == "j30" ]; then
    optfile=$datadir/${b}opt.sm
    optfiletmp=$datadir/${b}opttmp.sm
    wget -O $optfiletmp https://www.om-db.wi.tum.de/psplib/files/${b}opt.sm
    iconv -f utf-8 -t utf-8 -c $optfiletmp > $optfile
    rm $optfiletmp
  else
    lbfile=$datadir/${b}lb.sm
    lbfiletmp=$datadir/${b}lbtmp.sm
    wget -O $lbfiletmp https://www.om-db.wi.tum.de/psplib/files/${b}lb.sm
    iconv -f utf-8 -t utf-8 -c $lbfiletmp > $lbfile
    rm $lbfiletmp
  fi

done

python ../script/tasks/task_aggregate_bounds.py psplib
