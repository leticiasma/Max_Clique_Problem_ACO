from unittest import main, TestCase
from graph import UndirectedGraph
from aco import ACOMaxClique, TauRange
import pathlib
import numpy as np

data_dir_path = pathlib.Path(__file__).parent / "data"


class TestACOMaxClique(TestCase):
    def setUp(self):
        test_data_path = data_dir_path / "graph_10n_10e.col"
        self.graph = UndirectedGraph.from_col_file(test_data_path)
        n_ants = 10
        n_its = 10
        self.evap_r = 0.05
        self.t_max = 0.9
        t_range = TauRange(0.1, self.t_max)
        self.alpha = 1
        self.aco = ACOMaxClique(
            self.graph, n_ants, n_its, self.evap_r, t_range, self.alpha
        )

    def test_init_pheromones(self):
        pheromones = self.aco._init_pheromones()
        expected_pheromones = [
            np.zeros(2),
            np.zeros(6),
            np.zeros(3),
            np.zeros(3),
            np.zeros(4),
            np.zeros(3),
            np.zeros(3),
            np.zeros(1),
            np.zeros(4),
            np.zeros(3),
        ]
        for array in expected_pheromones:
            array.fill(self.t_max)

        for array_idx, my_array in enumerate(expected_pheromones):
            self.assertTrue((my_array == pheromones[array_idx]).all())

    def test_init_tau_factor(self):
        pheromones = self.aco._init_pheromones()
        initial_node = 3
        candidates = list(self.graph.ordered_neighboors(initial_node))
        cands_t_factor = self.aco._initialize_tau_factor(
            candidates, pheromones, initial_node
        )
        expected_cands_t_factor = {cand: self.t_max for cand in candidates}
        self.assertDictEqual(expected_cands_t_factor, cands_t_factor)

    def test_calc_probs_for_candidates(self):
        pheromones = self.aco._init_pheromones()
        initial_node = 3
        candidates = list(self.graph.ordered_neighboors(initial_node))
        cands_t_factor = self.aco._initialize_tau_factor(
            candidates, pheromones, initial_node
        )

        alpha_factor = self.t_max * self.alpha
        total_factor = alpha_factor * len(candidates)
        expected_value = alpha_factor / total_factor
        expected_probs = [expected_value for i in range(len(candidates))]

        probs = self.aco._calc_probs_for_candidates(candidates, cands_t_factor)

        self.assertListEqual(expected_probs, probs)

    def test_candidates_lose_a_member_after_chosing(self):
        pheromones = self.aco._init_pheromones()
        initial_node = 3
        candidates = list(self.graph.ordered_neighboors(initial_node))
        initial_len = len(candidates)
        cands_t_factor = self.aco._initialize_tau_factor(
            candidates, pheromones, initial_node
        )
        _ = self.aco._choose_candidate(candidates, cands_t_factor)
        self.assertTrue(initial_len - 1 == len(candidates))

    def test_can_update_candidates(self):
        candidates = [1, 2, 3, 4, 5]
        ordered_neighboors = (2, 3, 4)
        expected_candidates = [2, 3, 4]
        new_candidates = self.aco._update_candidates(
            candidates, ordered_neighboors
        )
        self.assertListEqual(expected_candidates, new_candidates)

    def test_can_evaporate_pheromones(self):
        persistence_rate = 1 - self.evap_r
        pheromones_list: list[np.ndarray] = list()
        pheromones_list.append(np.array([0.9, 0.9, 0.8]))
        pheromones_list.append(np.array([0.9, 0.8, 0.5]))

        expected_pheromones = [
            m_array * persistence_rate for m_array in pheromones_list
        ]

        self.aco._evaporate_pheromones(pheromones_list)

        for exp_array, true_array in zip(expected_pheromones, pheromones_list):
            self.assertTrue((exp_array == true_array).all())

    def test_can_deposit_pheromones(self):
        curr_max_clique = [2, 3, 5, 9]
        cycle_max_clique = [4, 6, 7]

        base_pheromone = 0.5
        base_pheromone_list = [base_pheromone]
        pheromones = [
            np.array(base_pheromone_list * 2),
            np.array(base_pheromone_list * 6),
            np.array(base_pheromone_list * 3),
            np.array(base_pheromone_list * 3),
            np.array(base_pheromone_list * 4),
            np.array(base_pheromone_list * 3),
            np.array(base_pheromone_list * 3),
            np.array(base_pheromone_list * 1),
            np.array(base_pheromone_list * 4),
            np.array(base_pheromone_list * 3),
        ]

        pheromone_to_add = 1 / (
            1 + len(curr_max_clique) - len(cycle_max_clique)
        )  # 0.5

        new_max_pheromone = base_pheromone + pheromone_to_add

        expected_pheromones = [
            np.array(base_pheromone_list * 2),
            np.array(base_pheromone_list * 6),
            np.array(base_pheromone_list * 3),
            np.array(
                [base_pheromone, new_max_pheromone, new_max_pheromone]
            ).clip(max=self.t_max),
            np.array(base_pheromone_list * 4),
            np.array(
                [new_max_pheromone, new_max_pheromone, base_pheromone]
            ).clip(max=self.t_max),
            np.array(
                [new_max_pheromone, base_pheromone, new_max_pheromone]
            ).clip(max=self.t_max),
            np.array(base_pheromone_list * 1),
            np.array(base_pheromone_list * 4),
            np.array(base_pheromone_list * 3),
        ]

        self.aco._deposit_pheromones(
            pheromones, cycle_max_clique, curr_max_clique
        )

        for exp_array, true_array in zip(expected_pheromones, pheromones):
            self.assertTrue((exp_array == true_array).all())

    def test_can_filter_cands_t_factor(self):
        candidates = [1, 2, 3, 4, 5]
        ordered_neighboors = [4, 5]
        cands_t_factor = {i: i for i in range(1, 12)}
        candidate_pheromones = np.array([0.9, 0.9])
        self.aco._filter_and_att_cands_t_factor(
            candidates, cands_t_factor, ordered_neighboors, candidate_pheromones
        )

        for i in range(6, 12):
            self.assertNotIn(i, cands_t_factor)
        
        for idx, i in enumerate([4,5]):
            self.assertEqual(cands_t_factor[i], i+candidate_pheromones[idx])
    
    def test_ant_can_find_a_clique(self):
        pheromones_list = self.aco._init_pheromones()
        initial_node = 4
        clique_found = self.aco._find_ant_clique(pheromones_list, initial_node)
        print(clique_found)
        self.assertTrue(len(clique_found) > 0)

if __name__ == "__main__":
    main()
