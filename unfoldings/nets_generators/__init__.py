"""
В этом модуле представлены генераторы различных сетей Петри, а именно:
1. mutual_exclusion - модель семафора с заданным количеством работников и флагов
2. dining_philosophers - модель задачи об обедающих философах (заданного их количества)
с возможной взаимной блокировкой.
"""

from .dining_philosophers import generate_dining_philosophers
from .mutual_exclusion import generate_mutual_exclusion

__all__ = [
    "generate_mutual_exclusion",
    "generate_dining_philosophers"
]
