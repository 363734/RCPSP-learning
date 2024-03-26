#! /bin/bash
# Download data from PSPLIB

source ../../rcpsp/bin/activate

datadir="../target/datas"
psplibdir="${datadir}/psplib"

mkdir -p $psplibdir

echo ":-: Download of PSPLIB data"
for b in "j30" "j60" "j90" "j120"; do
  echo ":-: Download of PSPLIB data: benchmark $b"

  mkdir -p $psplibdir/$b

  wget -O $psplibdir/$b/$b.zip https://www.om-db.wi.tum.de/psplib/files/$b.sm.zip
  unzip $psplibdir/$b/$b.zip -d $psplibdir/$b/
  rm $psplibdir/$b/$b.zip

  hrsfile=$psplibdir/${b}hrs.sm
  hrsfiletmp=$psplibdir/${b}hrstmp.sm
  wget -O $hrsfiletmp https://www.om-db.wi.tum.de/psplib/files/${b}hrs.sm
  iconv -f utf-8 -t utf-8 -c $hrsfiletmp > $hrsfile
  rm $hrsfiletmp

  if [ $b == "j30" ]; then
    optfile=$psplibdir/${b}opt.sm
    optfiletmp=$psplibdir/${b}opttmp.sm
    wget -O $optfiletmp https://www.om-db.wi.tum.de/psplib/files/${b}opt.sm
    iconv -f utf-8 -t utf-8 -c $optfiletmp > $optfile
    rm $optfiletmp
  else
    lbfile=$psplibdir/${b}lb.sm
    lbfiletmp=$psplibdir/${b}lbtmp.sm
    wget -O $lbfiletmp https://www.om-db.wi.tum.de/psplib/files/${b}lb.sm
    iconv -f utf-8 -t utf-8 -c $lbfiletmp > $lbfile
    rm $lbfiletmp
  fi

done

python ../script/tasks/task_aggregate_bounds.py psplib
