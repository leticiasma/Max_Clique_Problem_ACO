import argparse
import pathlib
from graph import UndirectedGraph

def config_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MaxCliqueACO")

    parser.add_argument("--data_path",
                        required=True,
                        help="The graph .col file")
    
    return parser


if __name__ == "__main__":
    parser = config_arg_parser()
    args = parser.parse_args()

    data_path = pathlib.Path(args.data_path)
    if not data_path.is_file():
        raise ValueError(f"{data_path} não existe!")
    
    if not data_path.suffix == ".col":
        raise ValueError(f"{data_path} não é um arquivo .col!")
    
    graph = UndirectedGraph.from_col_file(data_path)