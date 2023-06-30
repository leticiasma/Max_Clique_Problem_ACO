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
        evap_r = 0.05
        self.t_max = 0.9
        t_range = TauRange(0.1, self.t_max)
        self.alpha = 1
        self.aco = ACOMaxClique(
            self.graph, n_ants, n_its, evap_r, t_range, self.alpha
        )

    def test_init_pheromones(self):
        pheromones = self.aco._init_pheromones()
        expected_pheromones = [
            np.zeros(2),
            np.zeros(5),
            np.zeros(3),
            np.zeros(3),
            np.zeros(3),
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
        candidates = [1,2,3,4,5]
        ordered_neighboors = (2,3,4)
        expected_candidates = [2,3,4]
        new_candidates = self.aco._update_candidates(candidates, ordered_neighboors)
        self.assertListEqual(expected_candidates, new_candidates)


if __name__ == "__main__":
    main()
