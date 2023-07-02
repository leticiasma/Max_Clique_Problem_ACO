import argparse
import pathlib
from graph import UndirectedGraph
from aco import TauRange, ACOMaxClique

import time
from multiprocessing import Lock, pool, current_process


def config_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MaxCliqueACO")

    parser.add_argument(
        "--data_path", required=True, help="The graph .col file"
    )

    parser.add_argument(
        "--t_min",
        required=False,
        default=0.1,
        type=float,
        help="The min pheromone on each target (float, default:0.1)",
    )

    parser.add_argument(
        "--t_max",
        required=False,
        default=0.9,
        type=float,
        help="The max pheromone on each target (float, default:0.9)",
    )

    parser.add_argument(
        "--n_ants",
        required=False,
        default=10,
        type=int,
        help="The number of ants to use (int, default:10)",
    )

    parser.add_argument(
        "--n_its",
        required=False,
        default=100,
        type=int,
        help="The number of iterations to run (int, default:100)",
    )

    parser.add_argument(
        "--evap_r",
        required=False,
        default=0.05,
        type=float,
        help="The pheromone evaporation rate (float, default:0.05)",
    )

    parser.add_argument(
        "--alpha",
        required=False,
        default=1,
        type=int,
        help="The pheromone factor weight (int, default:1)",
    )

    parser.add_argument(
        "--n_p",
        required=False,
        default=1,
        type=int,
        help="Max number of processes to use (int default: 1)",
    )

    parser.add_argument(
        "--n_r",
        required=False,
        default=1,
        type=int,
        help="Number of runs (int, default: 1)",
    )

    parser.add_argument(
        "--t_dir",
        required=False,
        default="./results",
        type=str,
        help="The target dir where to save the results for each run of --n_r. \
                            (str, default: ./results)",
    )

    return parser


def check_between_0_and_1(name, value):
    if not (value >= 0 and value <= 1):
        raise ValueError(f"{name} ({value}) deve estar no intervalo [0, 1]!")


def check_positive_integer(name, value):
    if not value > 0:
        raise ValueError(f"{name} ({value}) deve ser um inteiro positivo!")


def validate_args(args) -> bool:
    data_path = pathlib.Path(args.data_path)
    if not data_path.is_file():
        raise ValueError(f"{data_path} não existe!")

    # if not data_path.suffix == ".col":
    #     raise ValueError(f"{data_path} não é um arquivo .col!")

    if args.t_min > args.t_max:
        raise ValueError(
            f"t_min ({args.t_min}) não pode ser maior do que t_max ({args.t_max})!"
        )

    # check_between_0_and_1("t_min", args.t_min)

    # check_between_0_and_1("t_max", args.t_max)

    check_between_0_and_1("evap_r", args.evap_r)

    check_positive_integer("n_ants", args.n_ants)

    check_positive_integer("n_its", args.n_its)

    check_positive_integer("alpha", args.alpha)


def run(args, run_id, timestr):
    data_path = pathlib.Path(args.data_path)
    graph = UndirectedGraph.from_col_file(data_path)
    t_range = TauRange(args.t_min, args.t_max)
    aco = ACOMaxClique(
        graph, args.n_ants, args.n_its, args.evap_r, t_range, args.alpha
    )
    maximum_clique = aco.find_maximum_clique()

    with lock:
        print(
            "(R:", run_id, ", ", current_process().name,
            ")\n Maximum Clique:", maximum_clique,
            " Total nodes: ", len(maximum_clique),
            flush=True,
        )
    
    aco.results_to_csv(pathlib.Path(args.t_dir) / f"{timestr}/run_{run_id}.csv")

def init(l):
    global lock
    lock = l

if __name__ == "__main__":
    parser = config_arg_parser()
    args = parser.parse_args()

    validate_args(args)
    print(args)
    
    write_results_lock = Lock()

    if args.n_p > args.n_r:
        args.n_p = args.n_r

    timestr = time.strftime("%Y%m%d-%H%M%S")
    with pool.Pool(initializer=init, initargs=(write_results_lock,), processes=args.n_p) as pool:
        pool.starmap(
            run,
            [(args, run_id, timestr) for run_id in range(args.n_r)],
        )
