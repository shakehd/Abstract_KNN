from _typeshed import Incomplete

def seed(seed: Incomplete | None = ...) -> None: ...
def rand(*shape): ...
def interp_decomp(A, eps_or_k, rand: bool = ...): ...
def reconstruct_matrix_from_id(B, idx, proj): ...
def reconstruct_interp_matrix(idx, proj): ...
def reconstruct_skel_matrix(A, k, idx): ...
def id_to_svd(B, idx, proj): ...
def estimate_spectral_norm(A, its: int = ...): ...
def estimate_spectral_norm_diff(A, B, its: int = ...): ...
def svd(A, eps_or_k, rand: bool = ...): ...
def estimate_rank(A, eps): ...
