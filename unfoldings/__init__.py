from .standard import build_prefix as standard_algorithm
from .n_safe import build_prefix as n_safe_algorithm

__all__ = [
    "standard_algorithm",
    "n_safe_algorithm",
]
