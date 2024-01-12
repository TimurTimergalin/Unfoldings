from pm4py.objects.petri_net.obj import Marking
from pm4py.objects.petri_net.utils import petri_utils

from abc import ABC, abstractmethod
from functools import cache


# Класс, представляющий локальную конфигурацию события в префиксе
class Configuration(ABC):
    @classmethod
    @abstractmethod
    def construct(cls, event):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    def __le__(self, other):
        return self < other or self == other

    # Вычисляет разметку сети в данной конфигурации (Mark)
    def mark(self):
        res = Marking()
        for e in self:
            post_set_marking = Marking(c.place for c in petri_utils.post_set(e))
            pre_set_marking = Marking(c.place for c in petri_utils.pre_set(e))

            res.update(post_set_marking)
            res.subtract(pre_set_marking)

        res._keep_positive()  # Убирает ключи со значением 0 (при корректной конфигурации отрицательных быть не может)
        return res


class CompareLengthConfiguration(Configuration):
    def __init__(self, event):
        self.events = set()
        self.init_events(event)

    @classmethod
    def construct(cls, event):
        return cls(event)

    def init_events(self, event):
        if event in self.events:
            return
        self.events.add(event)
        for c in petri_utils.pre_set(event):
            self.init_events(c.input_event)

    def __iter__(self):
        return iter(self.events)

    def __lt__(self, other):
        return len(self.events) < len(other.events)

    def __eq__(self, other):
        return len(self.events) == len(other.events)


class CompareLengthCachedConfiguration(CompareLengthConfiguration):
    @classmethod
    @cache
    def construct(cls, event):
        return super().construct(event)
