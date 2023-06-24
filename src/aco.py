from graph import UndirectedGraph

class TauRange:
    def __init__(self, t_min:float, t_max:float) -> None:
        self._t_max = t_max
        self._t_min = t_min
    
    @property
    def t_max(self) -> float:
        return self._t_max
    
    @property
    def t_min(self) -> float:
        return self._t_min

class ACOMaxClique:
    def __init__(self, graph:UndirectedGraph, n_ants:int, n_its:int, 
                 evap_r:float, t_range:TauRange, alpha:int):
        self._graph = graph
        self._n_ants = n_ants
        self._n_its = n_its
        self._evap_rate = evap_r
        self._t_range = t_range
        self._alpha = alpha