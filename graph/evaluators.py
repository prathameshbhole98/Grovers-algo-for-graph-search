from typing import Dict, List, Set, Tuple
from concurrent import futures
import itertools

#import graph_types as t
from graph import graph_types as t


class HamiltonianEvaluator:
    def __init__(self, edges: List[t.edge]):
       
        self.edges: List[t.edge] = edges
        self.vertices: Set[t.vertex] = {v for e in self.edges for v in e}

    def is_hamiltonian(self, edges: List[t.edge]) -> bool:
        
       
        if len(edges) != len(self.vertices):
            return False

        
        included_vertices = {v for e in edges for v in e}
        if included_vertices != self.vertices:
            return False

        
        vertex_meta = {v: [0, v] for v in included_vertices}
        for e_from, e_to in edges:
            leader = min(vertex_meta[e_from][1], vertex_meta[e_to][1])

            vertex_meta[e_from][1] = leader
            vertex_meta[e_from][0] += 1
            vertex_meta[e_to][1] = leader
            vertex_meta[e_to][0] += 1

        first_leader = next(iter(vertex_meta.values()))[1]
        for degree, leader in vertex_meta.values():
            if degree != 2 or leader != first_leader:
                return False
        return True

    def generate_truth_table(self) -> Dict[Tuple[t.edge, ...], bool]:
        
        executor = futures.ProcessPoolExecutor()
        iter1, iter2 = itertools.tee(itertools.combinations(self.edges,
                                                            len(self.vertices)))
        result = {e: is_ham for e, is_ham in zip(iter1, executor.map(self.is_hamiltonian, iter2))}
        return result
