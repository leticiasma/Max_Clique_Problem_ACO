DATA_PATH = ../data/brock800_4.clq
T_MIN = 0.1
T_MAX = 6
N_ANTS = 10
N_ITS = 100
EVAP_R = 0.1
ALPHA = 1
N_RUNS = 2
N_PROCESSES = 2
DATASET_NAME = brock800_4
RESULTS_TARGET_DIR = ../results/$(DATASET_NAME)

test:
	coverage run -m unittest discover tests
	coverage html

run:
	python3 main.py --data_path $(DATA_PATH) --t_min $(T_MIN) --t_max $(T_MAX) --n_ants $(N_ANTS) \
	--n_its $(N_ITS) --evap_r $(EVAP_R) --alpha $(ALPHA) --n_p $(N_PROCESSES) --n_r $(N_RUNS) \
	--t_dir $(RESULTS_TARGET_DIR)