from functools import partial
from itertools import chain, zip_longest

from pm4py.objects.petri_net.utils import petri_utils

from .abstract import Configuration, OrderSettings
from .config_length_utils import ConfigLength


class FoataConfiguration(Configuration):
    """Представление конфигурации в виде "слоев", соответствующих Фоатовской нормальной форме"""

    def __init__(self, event, save_length=None):
        self.events = []
        met = set()
        self.init_events(event, met)

        if save_length is not None:
            save_length.save(event, len(met))

    def init_events(self, event, met, before=0):
        if event in met:
            return
        met.add(event)

        if before == 0:
            self.events.insert(0, [event])
            before += 1
        else:
            self.events[before - 1].append(event)

        for c in petri_utils.pre_set(event):
            self.init_events(c.input_event, met, before - 1)

    def __iter__(self):
        return chain.from_iterable(self.events)

    def __len__(self):
        return sum(1 for _ in self)

    def __repr__(self):
        return repr(self.events)


def _cmp_from_operators(o1, o2):
    if o1 < o2:
        return -1
    if o1 > o2:
        return 1
    return 0


def lex_order(events):
    return sorted(events, key=lambda e: e.net_label)


def compare_lex(seq1, seq2):
    for f, s in zip_longest(seq1, seq2):
        if f is None:  # seq1 - префикс seq2
            return -1
        if s is None:  # seq2 - префикс seq1
            return 1

        # fi = id(f.transition)
        # si = id(s.transition)

        cmp = _cmp_from_operators(f.net_label, s.net_label)
        if cmp != 0:
            return cmp

    return 0


def cmp_events(e1, e2, config_length, *, config1=None, config2=None, **kwargs):
    if config1 is not None and not config_length.calculated(e1):
        config_length.save(e1, len(config1))
    if config2 is not None and not config_length.calculated(e2):
        config_length.save(e2, len(config2))

    # Конфигурации не вычисляются, если уже посчитана длина - возможно, сравнения длин будет достаточно
    c1 = config1 if config_length.calculated(e1) else FoataConfiguration(e1, config_length)
    c2 = config2 if config_length.calculated(e2) else FoataConfiguration(e2, config_length)

    # Сравнение длин
    l1 = config_length(e1)
    l2 = config_length(e2)

    l_cmp = l1 - l2
    if l_cmp != 0:
        return l_cmp

    # Считаем не посчитанные конфигурации
    if c1 is None:
        c1 = FoataConfiguration(e1, config_length)

    if c2 is None:
        c2 = FoataConfiguration(e2, config_length)

    # Сравнение в лексикографическом порядке
    total_cmp = compare_lex(lex_order(c1), lex_order(c2))

    if total_cmp != 0:
        return total_cmp

    # Сравнение нормальных форм
    for f, s in zip_longest(c1.events, c2.events):
        if f is None:  # seq1 - префикс seq2
            return -1
        if s is None:  # seq2 - префикс seq1
            return 1

        cmp = compare_lex(lex_order(f), lex_order(s))

        if cmp != 0:
            return cmp

    return 0


class FoataOrderSettings(OrderSettings):
    """Настройки порядка, при которых конфигурации сравниваются по Фоатовской нормальной форме"""

    def __init__(self):
        config_length = ConfigLength(FoataConfiguration)
        self.conf = partial(FoataConfiguration, save_length=config_length)
        self.cmp = partial(cmp_events, config_length=config_length)

    def config(self, event):
        return self.conf(event)

    def cmp_events(self, e1, e2, **kwargs):
        """
        Принимаемые подсказки:
            config1 - конфигурация e1. Если длина конфигурации e1 не была посчитана жо этого, вместо вычисления
            конфигурации будет использована длина config1. Если длины e1 и e2 равны, вместо вычисления конфигурации
            будет использована config1.
            config2 - конфигурация e2. Используется аналогично config1
        """
        return self.cmp(e1, e2, **kwargs)
