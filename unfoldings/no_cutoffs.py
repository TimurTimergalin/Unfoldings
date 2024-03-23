from pm4py.objects.petri_net.utils import petri_utils

from alg import Co, PriorityQueue, update_possible_extensions
from obj import Prefix, Event, Condition

from order_settings import BasicOrderSettings

from itertools import chain


def build_unfolding(net, m0, event_count=20):
    settings = BasicOrderSettings()
    res = Prefix(net.name)
    e = Event(None)  # "Изначальное" событие \bot. Его post_set-ом будут условия, соответствующе начальной маркировке
    bot = e
    res.add_event(e)

    co = Co()
    pe = PriorityQueue(settings.cmp_events)

    for p in m0.elements():  # Добавление условий, соответствующих начальной разметке
        c = Condition(p)
        res.add_condition(c)
        petri_utils.add_arc_from_to(e, c, res)
        res.add_starting_condition(c)

    co.update(e, res.places)
    update_possible_extensions(pe, e, net.transitions, co)

    for _ in range(event_count):
        if not pe:
            break

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
        transitions = set(chain.from_iterable(petri_utils.post_set(x) for x in postset))
        update_possible_extensions(pe, e, transitions, co)

    for a in bot.out_arcs:
        a.target.in_arcs.remove(a)
        res.arcs.remove(a)

    res.transitions.remove(bot)

    return res
