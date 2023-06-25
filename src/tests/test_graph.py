from unittest import main, TestCase
from graph import UndirectedGraph
import pathlib

data_dir_path = pathlib.Path(__file__).parent / "data"

class TestGraph(TestCase):
    def test_correct_neighboors(self):
        test_data_path = data_dir_path / "data_test.col"
        graph = UndirectedGraph.from_col_file(test_data_path)
        expected_neighboors = (1, 2)
        self.assertTupleEqual(graph.ordered_neighboors(3), expected_neighboors)
    
    def test_correct_ordered_neighboors(self):
        test_data_path = data_dir_path / "data_test.col"
        graph = UndirectedGraph.from_col_file(test_data_path)
        expected_neighboors = (1, 2)
        self.assertTupleEqual(graph.ordered_neighboors(3), expected_neighboors)
    
    def test_correct_neighboors_repeated_edges(self):
        test_data_path = data_dir_path / "repeated_edges.col"
        graph = UndirectedGraph.from_col_file(test_data_path)
        expected_neighboors = (2,)
        self.assertTupleEqual(graph.ordered_neighboors(1), expected_neighboors)
        
        expected_neighboors = (2, 3, 5)
        self.assertTupleEqual(graph.ordered_neighboors(4), expected_neighboors)
    
    def test_get_n_nodes(self):
        test_data_path = data_dir_path / "repeated_edges.col"
        graph = UndirectedGraph.from_col_file(test_data_path)
        expected_n_nodes = 5
        self.assertEqual(expected_n_nodes, graph.num_nodes)
    
    def test_get_n_edges(self):
        test_data_path = data_dir_path / "repeated_edges.col"
        graph = UndirectedGraph.from_col_file(test_data_path)
        expected_n_edges = 5
        self.assertEqual(expected_n_edges, graph.num_edges)
    
    def test_get_random_node_id(self):
        test_data_path = data_dir_path / "repeated_edges.col"
        graph = UndirectedGraph.from_col_file(test_data_path)
        node_id_range = range(1, 6)
        self.assertIn(graph.random_node_id(), node_id_range)
    
    def test_non_existent_node_has_none_neighboors(self):
        test_data_path = data_dir_path / "repeated_edges.col"
        graph = UndirectedGraph.from_col_file(test_data_path)
        self.assertIsNone(graph.n_neighboors(17))

if __name__ == "__main__":
    main()