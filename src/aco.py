from graph import UndirectedGraph
import numpy as np
import random


class TauRange:
    def __init__(self, t_min: float, t_max: float) -> None:
        self._t_max = t_max
        self._t_min = t_min

    @property
    def t_max(self) -> float:
        return self._t_max

    @property
    def t_min(self) -> float:
        return self._t_min


class ACOMaxClique:
    def __init__(
        self,
        graph: UndirectedGraph,
        n_ants: int,
        n_its: int,
        evap_r: float,
        t_range: TauRange,
        alpha: int,
    ):
        self._graph = graph
        self._n_ants = n_ants
        self._n_its = n_its
        self._evap_rate = evap_r
        self._t_range = t_range
        self._alpha = alpha

    def find_maximum_clique(self) -> list:
        """
        Tenta encontrar o maior clique possível ao simular caminhamentos de formigas de acordo
        com os feromônios que elas vão deixando no caminho.
        """
        pheromones_list = self._init_pheromones()

        final_max_clique = list()
        for _ in range(self._n_its):
            cycle_max_clique = list()

            for _ in range(self._n_ants):
                curr_ant_clique = self._find_ant_clique(pheromones_list)

                if len(curr_ant_clique) > len(cycle_max_clique):
                    cycle_max_clique = curr_ant_clique

            self._evaporate_pheromones(pheromones_list)
            self._deposit_pheromones(
                pheromones_list, cycle_max_clique, final_max_clique
            )

            if len(cycle_max_clique) > len(final_max_clique):
                final_max_clique = cycle_max_clique

        return final_max_clique

    def _find_ant_clique(self, pheromones_list: list[np.ndarray]) -> list:
        """
        Faz uma formiga caminhar pelo grafo e encontrar um clique.
        """
        curr_ant_clique = list()

        random_node = self._graph.random_node_id()
        curr_ant_clique.append(random_node)

        candidates = list(self._graph.ordered_neighboors(random_node))

        cands_t_factor = self._initialize_tau_factor(
            candidates, pheromones_list, random_node
        )
        while len(candidates) > 0:
            curr_candidate = self._choose_candidate(candidates, cands_t_factor)
            curr_ant_clique.append(curr_candidate)

            ordered_neighboors = self._graph.ordered_neighboors(curr_candidate)

            candidates = self._update_candidates(candidates, ordered_neighboors)

            self._filter_and_att_cands_t_factor(
                pheromones_list,
                candidates,
                cands_t_factor,
                curr_candidate,
                ordered_neighboors,
            )

        return curr_ant_clique

    def _update_candidates(self, candidates: list, ordered_neighboors: tuple):
        new_candidates = list(set(candidates).intersection(set(ordered_neighboors)))
        return new_candidates

    def _init_pheromones(self) -> list[np.ndarray]:
        """
        Inicia os feromônios para cada aresta.
        Retorna uma lista de np.arrays em que o índice na lista representa o índice -1 do nó
        de origem e os np.arrays possuem os feromônios das arestas que se ligam
        aos nós vizinhos do nó em ordem de índice.

        Por exemplo: Se o nó 1 tem como vizinhos os nós {7,2,5,8,3},
        então o seu np.array associado tem 5 posições em que as posições
        representam os feromônios para das arestas para os nós na seguinte ordem:
        [2,3,5,7,8]. Além disso, esse np.array estará no índice 0 da lista.
        Isso é feito pois o índice dos nós no arquivo de entrada começa em 1.
        """
        pheromones_list = list()
        for node_idx in range(1, self._graph.num_nodes + 1):
            edges_pheromones = np.zeros(self._graph.n_neighboors(node_idx))
            edges_pheromones.fill(self._t_range.t_max)
            pheromones_list.append(edges_pheromones)

        return pheromones_list

    def _initialize_tau_factor(
        self, candidates: list, pheromones_list: list, random_node: int
    ) -> dict:
        """
        Inicializa o fator de feromônio (tau) para cada candidato.
        """
        candidates_tau_factor = dict()
        ordered_neighboors = self._graph.ordered_neighboors(random_node)
        for candidate in candidates:
            candidate_idx = ordered_neighboors.index(candidate)
            tau_factor = pheromones_list[random_node][candidate_idx]
            candidates_tau_factor[candidate] = tau_factor

        return candidates_tau_factor

    def _choose_candidate(self, candidates: list, cand_tau_factor: dict) -> int:
        """
        Escolhe um candidato de candidates de acordo com probabilidades que
        dependem dos feromônios contidos em cand_tau_factor.
        Remove o candidato em candidates.
        """
        if len(candidates) == 1:
            return candidates.pop()

        probs = self._calc_probs_for_candidates(candidates, cand_tau_factor)
        candidate = random.choices(candidates, probs)[0]
        candidates.remove(candidate)
        return candidate

    def _calc_probs_for_candidates(
        self, candidates: list, cand_tau_factor: dict
    ) -> list:
        """
        Retorna uma lista de probabilidades para os candidatos em candidates
        """
        alpha_factors = [
            cand_tau_factor[cand] ** self._alpha for cand in candidates
        ]
        alpha_factors_sum = sum(alpha_factors)
        probs = [
            alpha_factors[cand_idx] / alpha_factors_sum
            for cand_idx in range(len(candidates))
        ]

        return probs

    def _filter_and_att_cands_t_factor(
        self,
        pheromones_list: list,
        candidates: list,
        cands_t_factor: dict,
        curr_candidate: int,
        ordered_neighboors: tuple,
    ):
        """
        Mantém em cands_t_factor apenas as chaves dos nós que estão em candidates.
        Para os nós j que permanecerem e forem vizinhos de curr_candidate,
        incrementa o seu t_factor baseado no feromônio associado à aresta que liga
        curr_candidate a j.
        """
        for node in cands_t_factor.keys():
            if node not in candidates:
                del cands_t_factor[node]
            else:
                if node in ordered_neighboors:
                    node_idx = ordered_neighboors.index(node)
                    cands_t_factor[node] += pheromones_list[curr_candidate][
                        node_idx
                    ]

    def _evaporate_pheromones(self, pheromones_list: list[np.ndarray]):
        """
        Evapora os feromônios das arestas. O feromônio nunca fica menor que o t_min
        definido em self._t_range.
        """
        persistence_rate = 1 - self._evap_rate
        for edges_pheromones in pheromones_list:
            new_pher = edges_pheromones * persistence_rate
            edges_pheromones = max([self._t_range.t_min, new_pher])

    def _deposit_pheromones(
        self,
        pheromones_list: list,
        cycle_max_clique: list,
        final_max_clique: list,
    ):
        """
        Deposita feromônios nas arestas do grafo induzido pelo cycle_max_clique.
        O feromônio nunca fica maior do que o t_max definido em self._t_range.
        O feromônio depositado é o resultado de:
        1/(1+len(final_max_clique)-len(cycle_max_clique))
        """
        pheromone_to_add = 1 / (
            1 + len(final_max_clique) - len(cycle_max_clique)
        )

        nodes_already_treated = set()
        for node in cycle_max_clique:
            node_neighs = self._graph.ordered_neighboors(node)
            for neigh_idx, neigh in enumerate(node_neighs):
                if (
                    neigh in cycle_max_clique
                    and neigh not in nodes_already_treated
                ):
                    curr_pher = pheromones_list[node - 1][neigh_idx]
                    new_pheromone = curr_pher + pheromone_to_add
                    pheromones_list[node - 1][neigh_idx] = min(
                        [new_pheromone, self._t_range.t_max]
                    )

            nodes_already_treated.add(node)
