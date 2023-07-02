#!/bin/bash
DATA_PATH="../data/p_hat700-2.clq"
T_MIN=0.1
T_MAX=6
N_ANTS=(10 15 20 25 30 35 40)
N_ITS=100
EVAP_R=0.1
ALPHA=1
N_RUNS=30
N_PROCESSES=2
DATASET_NAME="p_hat700"
RESULTS_TARGET_DIR="../results/$DATASET_NAME"

for i in "${N_ANTS[@]}"
do
    echo "Iniciando com N_ANTS = $i"
	python3 main.py --data_path $DATA_PATH --t_min $T_MIN --t_max $T_MAX --n_ants $i \
	--n_its $N_ITS --evap_r $EVAP_R --alpha $ALPHA --n_p $N_PROCESSES --n_r $N_RUNS \
	--t_dir $RESULTS_TARGET_DIR
done