from pm4py.objects.petri_net.utils import petri_utils

from alg import Co, PriorityQueue, update_possible_extensions
from obj import Prefix, Event, Condition

from itertools import chain


# Строит развертку сети Петри по алгоритму МакМиллана (но с настраиваемым порядком на конфигурациях)
# net - сеть Петри
# m0 - начальная разметка
# config_type - тип конфигурации
def build_prefix(net, m0, order_settings, cutoff_settings, event_count=None):
    if event_count is not None and event_count <= 0:
        raise ValueError("event count must be positive")

    res = Prefix(net.name)  # В res будет находиться итоговый префикс

    # В этом словаре разметкам будут сопоставляться события, локальные конфигурации которых минимальны
    # и имеют эту разметку.
    # Он будет использоваться для того, чтобы узнать, является ли то или иное событие cut-off

    e = Event(None)  # "Изначальное" событие \bot. Его post_set-ом будут условия, соответствующе начальной маркировке
    bot = e
    res.add_event(e)

    co = Co()
    pe = PriorityQueue(order_settings.cmp_events)

    for p in m0.elements():  # Добавление условий, соответствующих начальной разметке
        c = Condition(p)
        res.add_condition(c)
        petri_utils.add_arc_from_to(e, c, res)
        res.add_starting_condition(c)

    # Обновление отношения co, очереди pe и словаря конфигураций
    co.update(e, res.places)
    cutoff_settings.update(e, order_settings, mark=m0)
    update_possible_extensions(pe, e, net.transitions, co)

    count = 0
    finished = True
    while pe:  # Пока к префиксу можно добавить новые события
        e, pre = pe.pop()  # Выбираем событие с минимальной длиной локальной конфигурации

        # Добавляем к префиксу выбранное событие и ребра к нему от условий в его preset-е
        res.add_event(e)
        for c in pre:
            petri_utils.add_arc_from_to(c, e, res)

        # Создаём условия, соответствующие позициям из post_set-а перехода, представленного выбранным событием
        postset = set()
        for a in e.transition.out_arcs:
            postset.add(a.target)
            for _ in range(a.weight):
                c = Condition(a.target)
                res.add_condition(c)
                petri_utils.add_arc_from_to(e, c, res)

        co.update(e, res.places)
        is_cutoff, hint = cutoff_settings.check_cutoff(e, order_settings)
        if not is_cutoff:
            cutoff_settings.update(e, order_settings, **hint)
            transitions = set(chain.from_iterable(petri_utils.post_set(x) for x in postset))
            update_possible_extensions(pe, e, transitions, co)
            count += 1
            if event_count is not None and pe and count >= event_count:
                finished = False
                break
        else:
            res.add_cutoff(e)

    # После процедуры удаляем событие bot из префикса - оно было нужно лишь при построении
    for a in bot.out_arcs:
        a.target.in_arcs.remove(a)
        res.arcs.remove(a)

    res.transitions.remove(bot)

    res.finished = finished

    return res
