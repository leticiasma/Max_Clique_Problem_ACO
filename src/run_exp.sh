#!/bin/bash
DATA_PATH="../data/brock800_4.clq"
T_MIN=0.1
T_MAX=6
N_ANTS=40
N_ITS=150
EVAP_R=(0.01 0.05 0.1 0.15 0.2)
ALPHA=1
N_RUNS=30
N_PROCESSES=3
DATASET_NAME="brock800_4"
RESULTS_TARGET_DIR="../results/$DATASET_NAME"

for i in "${EVAP_R[@]}"
do
    echo "Iniciando com EVAP_R= $i"
	python3 main.py --data_path $DATA_PATH --t_min $T_MIN --t_max $T_MAX --n_ants $N_ANTS \
	--n_its $N_ITS --evap_r $i --alpha $ALPHA --n_p $N_PROCESSES --n_r $N_RUNS \
	--t_dir $RESULTS_TARGET_DIR
done
