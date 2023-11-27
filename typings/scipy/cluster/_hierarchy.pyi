from typing import ClassVar

__test__: dict

class Heap:
    __pyx_vtable__: ClassVar[PyCapsule] = ...
    def __init__(self, *args, **kwargs) -> None: ...
    def change_value(self, *args, **kwargs): ...
    def get_min(self, *args, **kwargs): ...
    def remove_min(self, *args, **kwargs): ...
    def __reduce__(self): ...

class LinkageUnionFind:
    __pyx_vtable__: ClassVar[PyCapsule] = ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __reduce__(self): ...

def calculate_cluster_sizes(*args, **kwargs): ...
def cluster_dist(*args, **kwargs): ...
def cluster_in(*args, **kwargs): ...
def cluster_maxclust_dist(*args, **kwargs): ...
def cluster_maxclust_monocrit(*args, **kwargs): ...
def cluster_monocrit(*args, **kwargs): ...
def cophenetic_distances(*args, **kwargs): ...
def fast_linkage(*args, **kwargs): ...
def get_max_Rfield_for_each_cluster(*args, **kwargs): ...
def get_max_dist_for_each_cluster(*args, **kwargs): ...
def inconsistent(*args, **kwargs): ...
def leaders(*args, **kwargs): ...
def linkage(*args, **kwargs): ...
def mst_single_linkage(*args, **kwargs): ...
def nn_chain(*args, **kwargs): ...
def prelist(*args, **kwargs): ...
