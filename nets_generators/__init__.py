"""
В этом модуле представлены генераторы различных сетей Петри, а именно:
1. mutual_exclusion - модель семафора с заданным количеством работников и флагов
2. dining_philosophers - модель задачи об обедающих философах (заданного их количества)
с возможной взаимной блокировкой.
"""

from .dining_philosophers import generate_dining_philosophers
from .mutual_exclusion import generate_mutual_exclusion
from .dining_philosophers_with_dict import generate_dining_philosophers_with_dict
from .milners_cyclic_scheduler import generate_milners_cyclic_scheduler

__all__ = [
    "generate_mutual_exclusion",
    "generate_dining_philosophers",
    "generate_dining_philosophers_with_dict",
    "generate_milners_cyclic_scheduler"
]
