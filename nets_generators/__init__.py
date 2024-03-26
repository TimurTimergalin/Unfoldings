"""
В этом модуле представлены генераторы различных сетей Петри, а именно:
1. mutual_exclusion - модель семафора с заданным количеством работников и флагов
2. dining_philosophers - модель задачи об обедающих философах (заданного их количества)
с возможной взаимной блокировкой.
"""

from .mutual_exclusion import generate_mutual_exclusion
from .dining_philosophers import generate_dining_philosophers
