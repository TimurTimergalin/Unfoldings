from pm4py.objects.petri_net.utils import petri_utils

from .prefix import NSafePrefix
from .event import NSafeEvent
from .condition import NSafeCondition
from .concurrency_relation import NSafeCo
from .possible_extensions import update_possible_extensions
from alg import PriorityQueue


# Построение префикса
# Алгоритм мало отличается от основного, для пояснений см. unfoldings/standard.py
def build_prefix(net, m0, order_settings, cutoff_settings):
    res = NSafePrefix(net.name)

    e = NSafeEvent(None, None)
    bot = e
    res.add_event(e)

    co = NSafeCo()
    pe = PriorityQueue(order_settings.cmp_events)

    for p in net.places:
        c = NSafeCondition(p, m0.get(p, 0))
        res.add_condition(c)
        petri_utils.add_arc_from_to(e, c, res)
        res.add_starting_condition(c)

    co.update(e, res.places)
    cutoff_settings.update(e, order_settings, mark=m0)
    update_possible_extensions(pe, e, net.transitions, co)

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

        co.update(e, res.places)

        is_cutoff, hint = cutoff_settings.check_cutoff(e, order_settings)
        if not is_cutoff:
            cutoff_settings.update(e, order_settings, **hint)
            update_possible_extensions(pe, e, net.transitions, co)
        else:
            res.add_cutoff(e)

    for a in bot.out_arcs:
        a.target.in_arcs.remove(a)
        res.arcs.remove(a)

    res.transitions.remove(bot)

    return res
