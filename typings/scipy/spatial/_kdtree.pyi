from ._ckdtree import cKDTree
from _typeshed import Incomplete

def minkowski_distance_p(x, y, p: int = ...): ...
def minkowski_distance(x, y, p: int = ...): ...

class Rectangle:
    maxes: Incomplete
    mins: Incomplete
    def __init__(self, maxes, mins) -> None: ...
    def volume(self): ...
    def split(self, d, split): ...
    def min_distance_point(self, x, p: float = ...): ...
    def max_distance_point(self, x, p: float = ...): ...
    def min_distance_rectangle(self, other, p: float = ...): ...
    def max_distance_rectangle(self, other, p: float = ...): ...

class KDTree(cKDTree):
    class node:
        def __init__(self, ckdtree_node: Incomplete | None = ...) -> None: ...
        def __lt__(self, other): ...
        def __gt__(self, other): ...
        def __le__(self, other): ...
        def __ge__(self, other): ...
        def __eq__(self, other): ...
    class leafnode(node):
        @property
        def idx(self): ...
        @property
        def children(self): ...
    class innernode(node):
        less: Incomplete
        greater: Incomplete
        def __init__(self, ckdtreenode) -> None: ...
        @property
        def split_dim(self): ...
        @property
        def split(self): ...
        @property
        def children(self): ...
    @property
    def tree(self): ...
    def __init__(self, data, leafsize: int = ..., compact_nodes: bool = ..., copy_data: bool = ..., balanced_tree: bool = ..., boxsize: Incomplete | None = ...) -> None: ...
    def query(self, x, k: int = ..., eps: int = ..., p: int = ..., distance_upper_bound=..., workers: int = ...): ...
    def query_ball_point(self, x, r, p: float = ..., eps: int = ..., workers: int = ..., return_sorted: Incomplete | None = ..., return_length: bool = ...): ...
    def query_ball_tree(self, other, r, p: float = ..., eps: int = ...): ...
    def query_pairs(self, r, p: float = ..., eps: int = ..., output_type: str = ...): ...
    def count_neighbors(self, other, r, p: float = ..., weights: Incomplete | None = ..., cumulative: bool = ...): ...
    def sparse_distance_matrix(self, other, max_distance, p: float = ..., output_type: str = ...): ...

def distance_matrix(x, y, p: int = ..., threshold: int = ...): ...
