from pm4py.objects.petri_net.utils import petri_utils

from .condition import NSafeCondition
from .event import NSafeEvent
from .possible_extensions import update_possible_extensions
from ...alg import PriorityQueue, Co
from ...decorations import IdleDecorations
from ...obj import Prefix


def build_prefix(net, m0, order_settings, cutoff_settings, decorations=None, event_count=None):
    """
    Строит канонический префикс развертки данной сети (при правильно определенном контексте срезания, за который
    отвечают аргументы order_settings и cutoff_settings)
    :param net: сеть Петри
    :param m0: начальная разметка net
    :param order_settings: настройки порядка
    :param cutoff_settings: настройки срезания
    :param decorations: декорации (опционально)
    :param event_count: максимальное количество событий в префиксе. Если построение префикса не закончится до того,
    как количество событий в префиксе превысит данное значение, построение префикса прекратится и значение флага
    finished будет False. Если не передать event_count, ограничения на количество событий не будет
    :return: префикс развертки
    """
    if event_count is not None and event_count <= 0:
        raise ValueError("event count must be positive")
    if decorations is None:
        decorations = IdleDecorations()
    res = Prefix(net.name)

    e = NSafeEvent(None, None)
    bot = e
    res.add_event(e)

    co = Co()
    pe = PriorityQueue(order_settings)

    # Начальные условия берутся из всех позиций изначальной сети
    for p in net.places:
        c = NSafeCondition(p, m0.get(p, 0))
        res.add_condition(c)
        petri_utils.add_arc_from_to(e, c, res)
        decorations.add_condition(c)
        decorations.add_starting_condition(c)

    co.update(e, res.places)
    cutoff_settings.update(e, order_settings, mark=m0)
    update_possible_extensions(pe, e, res.places, co)

    count = 0
    finished = True
    while pe:
        e, pre = pe.pop()
        res.add_event(e)

        preset_weight = {x.source: x.weight for x in e.transition.in_arcs}
        postset_weight = {x.target: x.weight for x in e.transition.out_arcs}

        for c in pre:
            petri_utils.add_arc_from_to(c, e, res)
            p = c.place
            # Единственное отличие от основного алгоритма - подсчёт количества маркеров в новых позициях
            dm = c.markers - preset_weight.get(p, 0) + postset_weight.get(p, 0)
            c = NSafeCondition(p, dm)
            res.add_condition(c)
            petri_utils.add_arc_from_to(e, c, res)
            decorations.add_condition(c)

        is_cutoff, hint = cutoff_settings.check_cutoff(e, order_settings)
        decorations.add_event(e)
        if not is_cutoff:
            concurrent_with = co.update(e, res.places)
            cutoff_settings.update(e, order_settings, **hint)
            update_possible_extensions(pe, e, concurrent_with, co)
            count += 1
            if event_count is not None and pe and count >= event_count:
                finished = False
                break
        else:
            res.add_cutoff(e)
            decorations.add_cutoff_event(e)

    for a in bot.out_arcs:
        a.target.in_arcs.remove(a)
        res.arcs.remove(a)

    res.transitions.remove(bot)
    res.finished = finished

    return res
