DATA_PATH = ../data/dsjc125.1.col
T_MIN = 0.1
T_MAX = 0.9
N_ANTS = 10
N_ITS = 100
EVAP_R = 0.05
ALPHA = 1

test:
	python3 -m unittest discover tests

run:
	python3 main.py --data_path $(DATA_PATH) --t_min $(T_MIN) --t_max $(T_MAX) --n_ants $(N_ANTS) \
	--n_its $(N_ITS) --evap_r $(EVAP_R) --alpha $(ALPHA)  