from __future__ import annotations
import pathlib

class UndirectedGraph:
    def __init__(self, num_nodes:int, num_edges:int) -> None:
        self._num_nodes = num_nodes
        self._num_edges = num_edges
        self._edge_dict = dict()
        
        #Indices começando com 1
        for i in range(1, num_nodes+1):
            self._edge_dict[i] = set()
    
    @property
    def num_nodes(self) -> int:
        return self._num_nodes

    @property
    def num_edges(self) -> int:
        return self._num_edges
    
    @property
    def edges(self) -> None:
        raise AttributeError("Não é possível acessar o container de arestas diretamente!")
    
    @edges.setter
    def edges(self, new_edges) -> None:
        raise AttributeError("Não é possível substituir o container de arestas!")
    
    def add_edge(self, origin_node:int, dest_node:int) -> None:
        """
        Adiciona uma aresta não direcionada entre origin_node e dest_node
        """
        if origin_node not in self._edge_dict or dest_node not in self._edge_dict:
            return
        
        self._edge_dict[origin_node].add(dest_node)
        self._edge_dict[dest_node].add(origin_node)
    
    def neighboors(self, node_id:int) -> set:
        """
        Retorna o conjunto de nós vizinhos de node_id. Se node_id não estiver cadastrado,
        """
        if node_id in self._edge_dict:
            return self._edge_dict[node_id]
        else:
            return None

    @classmethod
    def from_col_file(cls, file_path:pathlib.Path) -> UndirectedGraph:
        graph_obj = None

        with open(file_path, "r") as col_file:
            while True:
                line = col_file.readline().strip()

                if not line:
                    break

                elif line.startswith("c"):
                    continue
                
                elif line.startswith("p"):
                    line_parts = line.split(" ")
                    num_nodes = int(line_parts[2])
                    num_edges = int(line_parts[3])
                    graph_obj = UndirectedGraph(num_nodes, num_edges)
                    print("Num nodes: ", num_nodes, " Num edges: ", num_edges)
                
                elif line.startswith("e"):
                    line_parts = line.split(" ")
                    origin_node = int(line_parts[1])
                    dest_node = int(line_parts[2])
                    graph_obj.add_edge(origin_node, dest_node)
                
                else:
                    print("WARNING: COULD NOT PARSE LINE: ", line)
                    continue
        
        return graph_obj
