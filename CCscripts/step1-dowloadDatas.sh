#! /bin/bash
# Download data from PSPLIB

source ../../rcpsp/bin/activate

#setup the structure of the project
python ../script/tasks/task_create_structure_of_project.py

#load datasets
bash bench_psplib_download.sh
python ../script/tasks/task_create_structure_of_project.py psplib

# TODO add new dataset here
