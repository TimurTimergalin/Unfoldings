from abc import ABC, abstractmethod

from pm4py.objects.petri_net.obj import Marking
from pm4py.objects.petri_net.utils import petri_utils


class OrderSettings(ABC):
    @property
    @abstractmethod
    def config(self):
        pass

    @property
    @abstractmethod
    def cmp_events(self):
        pass


# Класс, представляющий локальную конфигурацию события в префиксе
class Configuration(ABC):
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    # Вычисляет разметку сети в данной конфигурации (Mark)
    def mark(self):
        res = Marking()
        for e in self:
            post_set_marking = e.postset_marking()
            pre_set_marking = e.preset_marking()

            res.update(post_set_marking)
            res.subtract(pre_set_marking)

        res._keep_positive()  # Убирает ключи со значением 0 (при корректной конфигурации отрицательных быть не может)
        return res
