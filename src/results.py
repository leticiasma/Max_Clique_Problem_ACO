import pathlib
from typing import Dict
import numpy as np


class Results:
    def __init__(self, num_nodes: int):
        self._clique_sizes_per_it: Dict[int, list] = dict()
        self._mean_pheromones: Dict[int, float] = dict()
        self._curr_it = 0
        self._curr_it_freqs: Dict[int, int] = dict()
        self._similarity_ratios: Dict[int, float] = dict()
        self._num_nodes = num_nodes
        self._all_cliques_found = set()
        self._num_cliques_found = 0

    def add_clique_found_at_it(self, clique: list, it: int):
        # Salvar o tamanho do clique no ciclo da it
        self._clique_sizes_per_it.setdefault(it, list()).append(len(clique))
        self._all_cliques_found.add(tuple(clique))
        self._num_cliques_found += 1

        if it != self._curr_it:
            curr_similarity = self._calc_curr_it_sim_ratio()
            self._similarity_ratios[self._curr_it] = curr_similarity

            self._curr_it = it
            self._curr_it_freqs = dict()

        for node in clique:
            if node not in self._curr_it_freqs:
                self._curr_it_freqs[node] = 0

            self._curr_it_freqs[node] += 1

    def _calc_curr_it_sim_ratio(self) -> float:
        total_freqs = 0
        for node_id in range(1, self._num_nodes + 1):
            node_freq = self._curr_it_freqs.get(node_id, 0)
            freq_numerator = node_freq * (node_freq - 1)
            total_freqs += freq_numerator

        curr_it_cliques = self._clique_sizes_per_it[self._curr_it]
        size_denominator = (len(curr_it_cliques) - 1) * (sum(curr_it_cliques))
        curr_similarity = total_freqs / size_denominator
        return curr_similarity

    def calc_mean_pheromones_at_it(self, pheromones: list[np.ndarray], it: int):
        total = 0
        total_edges = 0
        for node_edges_phers in pheromones:
            total += node_edges_phers.sum()
            total_edges += node_edges_phers.shape[0]

        self._mean_pheromones[it] = total / total_edges

    def to_csv(self, path: pathlib.Path, delimiter=","):
        # So it has a similarity measure at the last it
        curr_similarity = self._calc_curr_it_sim_ratio()
        self._similarity_ratios[self._curr_it] = curr_similarity
        
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as m_file:
            header = delimiter.join(
                "it max_clique max_cycle_clique mean_p similarity re_samp_ratio".split()
            )
            m_file.write(header)
            m_file.write("\n")

            re_samp_ratio = self._re_sampling_ratio()

            curr_max_clique_size = 0
            for it in range(1, self._curr_it + 1):
                it_results = list()

                it_results.append(it)

                cycle_max_clique = max(self._clique_sizes_per_it[it])
                if cycle_max_clique > curr_max_clique_size:
                    curr_max_clique_size = cycle_max_clique

                it_results.append(curr_max_clique_size)
                it_results.append(cycle_max_clique)

                it_results.append(self._mean_pheromones[it])
                it_results.append(self._similarity_ratios[it])
                it_results.append(re_samp_ratio)

                line = delimiter.join([str(el) for el in it_results])

                m_file.write(line)
                m_file.write("\n")

    def _re_sampling_ratio(self) -> float:
        n_diff_cliques_found = len(self._all_cliques_found)
        re_samp_ratio = (
            self._num_cliques_found - n_diff_cliques_found
        ) / self._num_cliques_found

        return re_samp_ratio
    
class ResultsAgg:
    def __init__(self):
        self.per_it_max_clique = dict()
        self.per_cycle_max_clique = dict()
        self.per_it_mean_p = dict()
        self.per_it_similarity = dict()
        self.per_run_re_samp_ratio = dict()
    
    def agg_files(self, paths:list[pathlib.Path], delimiter=","):
        self.per_it_max_clique = dict()
        self.per_cycle_max_clique = dict()
        self.per_it_mean_p = dict()
        self.per_it_similarity = dict()
        self.per_run_re_samp_ratio = dict()


        for path_id, path in enumerate(paths):
            path = pathlib.Path(path)
            with open(path, 'r') as file:
                for l_idx, line in enumerate(file): 
                    if l_idx == 0:
                        continue

                    data:list = line.split(delimiter)
                    curr_it = int(data[0])
                    self.per_it_max_clique.setdefault(curr_it, list()).append(int(data[1]))
                    self.per_cycle_max_clique.setdefault(curr_it, list()).append(int(data[2]))
                    self.per_it_mean_p.setdefault(curr_it, list()).append(float(data[3]))
                    self.per_it_similarity.setdefault(curr_it, list()).append(float(data[4]))
                    self.per_run_re_samp_ratio[path_id] = float(data[5]) 