from functools import partial

from pm4py.objects.petri_net.utils import petri_utils

from .abstract import Configuration, OrderSettings
from .config_length_utils import ConfigLength


class BasicConfiguration(Configuration):
    """Представление конфигурации в виде множества событий"""

    def __init__(self, event, save_length=None):
        self.events = set()
        self.init_events(event)

        if save_length is not None:
            save_length.save(event, len(self.events))

    def init_events(self, event):
        if event in self.events:
            return
        self.events.add(event)
        for c in petri_utils.pre_set(event):
            self.init_events(c.input_event)

    def __iter__(self):
        return iter(self.events)

    def __len__(self):
        return len(self.events)

    @staticmethod
    def cmp_events(e1, e2, config_length, *, config1=None, config2=None, **kwargs):
        if config1 is not None and not config_length.calculated(e1):
            config_length.save(e1, len(config1))
        if config2 is not None and not config_length.calculated(e2):
            config_length.save(e2, len(config2))

        l1 = config_length(e1)
        l2 = config_length(e2)
        return l1 - l2

    def __repr__(self):
        return repr(self.events)


class BasicOrderSettings(OrderSettings):
    """Настройки порядка, при которых конфигурации сравниваются по длине"""

    def __init__(self):
        config_length = ConfigLength(BasicConfiguration)
        self.conf = partial(BasicConfiguration, save_length=config_length)
        self.cmp = partial(BasicConfiguration.cmp_events, config_length=config_length)

    def config(self, event):
        return self.conf(event)

    def cmp_events(self, e1, e2, **kwargs):
        """
        Принимаемые подсказки:
            config1 - конфигурация e1. Если длина конфигурации e1 не была посчитана жо этого, вместо вычисления
            конфигурации будет использована длина config1
            config2 - конфигурация e2. Используется аналогично config1
        """
        return self.cmp(e1, e2, **kwargs)
