from pm4py.objects.petri_net.utils import petri_utils

from alg import Co, PriorityQueue, update_possible_extensions
from obj import Prefix, Event, Condition


# Строит развертку сети Петри по алгоритму МакМиллана (но с настраиваемым порядком на конфигурациях)
# net - сеть Петри
# m0 - начальная разметка
# config_type - тип конфигурации
def build_prefix(net, m0, settings):
    res = Prefix(net.name)  # В res будет находиться итоговый префикс

    # В этом словаре разметкам будут сопоставляться события, локальные конфигурации которых минимальны
    # и имеют эту разметку.
    # Он будет использоваться для того, чтобы узнать, является ли то или иное событие cut-off
    min_by_mark = {}

    e = Event(None)  # "Изначальное" событие \bot. Его post_set-ом будут условия, соответствующе начальной маркировке
    bot = e
    res.add_event(e)

    co = Co()
    pe = PriorityQueue(settings.cmp_events)

    for p in m0.elements():  # Добавление условий, соответствующих начальной разметке
        c = Condition(p)
        res.add_condition(c)
        petri_utils.add_arc_from_to(e, c, res)

    # Обновление отношения co, очереди pe и словаря конфигураций
    co.update(e, res.places)
    min_by_mark[m0] = e
    update_possible_extensions(pe, e, net.transitions, co)

    while pe:  # Пока к префиксу можно добавить новые события
        e, pre = pe.pop()  # Выбираем событие с минимальной длиной локальной конфигурации

        # Добавляем к префиксу выбранное событие и ребра к нему от условий в его preset-е
        res.add_event(e)
        for c in pre:
            petri_utils.add_arc_from_to(c, e, res)

        # Создаём условия, соответствующие позициям из post_set-а перехода, представленного выбранным событием
        for a in e.transition.out_arcs:
            for _ in range(a.weight):
                c = Condition(a.target)
                res.add_condition(c)
                petri_utils.add_arc_from_to(e, c, res)

        co.update(e, res.places)
        config = settings.config(e)
        m = config.mark()
        if m not in min_by_mark or settings.cmp_events(min_by_mark[m], e) >= 0:
            update_possible_extensions(pe, e, net.transitions, co)
            min_by_mark[m] = e

    # После процедуры удаляем событие bot из префикса - оно было нужно лишь при построении
    for a in bot.out_arcs:
        a.target.in_arcs.remove(a)
        res.arcs.remove(a)

    res.transitions.remove(bot)

    return res
