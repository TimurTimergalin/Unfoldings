"""
В этом модуле реализованы классы, расширяющие представления сети Петри библиотеки pm4py:
1. Event расширяет PetriNet.Transition и представляет событие развертки
2. Condition расширяет PetriNet.Place и представляет условие разверкти
3. Prefix расширяет PetriNet и представляет префикс развертки
"""

from .condition import *
from .event import *
from .prefix import *


__all__ = [
    "Condition",
    "Event",
    "Prefix"
]
