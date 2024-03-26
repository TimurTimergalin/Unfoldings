"""
В этом модуле представлены реализации алгоритмов построения префиксов развертки, а именно:
1. standard - стандартный алгоритм построения канонических префиксов
2. n_safe - построение канонических префиксов развертки сети, трансформированной в безопасную.
"""

from .standard import build_prefix as standard_algorithm
from .n_safe import build_prefix as n_safe_algorithm

__all__ = [
    "standard_algorithm",
    "n_safe_algorithm",
]
