from pm4py.objects.petri_net.utils import petri_utils

from .abstract import Configuration, OrderSettings
from .config_length_utils import ConfigLength

from functools import partial


class BasicConfiguration(Configuration):
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
    def cmp_events(e1, e2, config_length, **kwargs):
        l1 = config_length(e1)
        l2 = config_length(e2)
        return l1 - l2

    def __repr__(self):
        return repr(self.events)


class BasicOrderSettings(OrderSettings):
    def __init__(self):
        config_length = ConfigLength(BasicConfiguration)
        self.conf = partial(BasicConfiguration, save_length=config_length)
        self.cmp = partial(BasicConfiguration.cmp_events, config_length=config_length)

    @property
    def config(self):
        return self.conf

    @property
    def cmp_events(self):
        return self.cmp
