from functools import partial
from itertools import zip_longest

from pm4py.objects.petri_net.utils import petri_utils

from settings import Settings
from settings.foata import FoataConfiguration, cmp_events
from settings.config_length_utils import ConfigLength

from pm4py.objects.petri_net.obj import Marking


class NSafeFoataConfiguration(FoataConfiguration):
    def mark(self):
        res = Marking()
        for e in self:
            post_set_marking = Marking({c.place: c.markers for c in petri_utils.post_set(e)})
            pre_set_marking = Marking({c.place: c.markers for c in petri_utils.pre_set(e)})

            res.update(post_set_marking)
            res.subtract(pre_set_marking)

        res._keep_positive()  # Убирает ключи со значением 0 (при корректной конфигурации отрицательных быть не может)
        return res


def lex_order(events):
    return sorted(events, key=lambda e: (id(e.transition), hash(e.marking)))


def compare_lex(seq1, seq2):
    for f, s in zip_longest(seq1, seq2):
        if f is None:  # seq1 - префикс seq2
            return -1
        if s is None:  # seq2 - префикс seq1
            return 1

        fi = id(f.transition)
        si = id(s.transition)

        cmp = fi - si
        if cmp != 0:
            return cmp

        fmi = hash(f.marking)
        smi = hash(s.marking)

        m_cmp = fmi - smi

        if m_cmp != 0:
            return cmp

    return 0


class NSafeSettings(Settings):
    def __init__(self):
        config_length = ConfigLength(NSafeFoataConfiguration)
        self.conf = partial(NSafeFoataConfiguration, save_length=config_length)
        self.cmp = partial(cmp_events, config_length=config_length, f_lex_order=lex_order, f_compare_lex=compare_lex)

    @property
    def config(self):
        return self.conf

    @property
    def cmp_events(self):
        return self.cmp
