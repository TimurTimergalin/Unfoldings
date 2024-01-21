from pm4py.objects.petri_net.utils import petri_utils

from .prefix import NSafePrefix
from .event import NSafeEvent
from .condition import NSafeCondition
from .concurrency_relation import NSafeCo
from .possible_extensions import update_possible_extensions
from alg import PriorityQueue


def build_prefix(net, m0, settings):
    res = NSafePrefix(net.name)

    min_by_mark = {}

    e = NSafeEvent(None, None)
    bot = e
    res.add_event(e)

    co = NSafeCo()
    pe = PriorityQueue(settings.cmp_events)

    for p in net.places:
        c = NSafeCondition(p, m0.get(p, 0))
        res.add_condition(c)
        petri_utils.add_arc_from_to(e, c, res)

    co.update(e, res.places)
    min_by_mark[m0] = e
    update_possible_extensions(pe, e, net.transitions, co)

    while pe:
        e, pre = pe.pop()
        res.add_event(e)

        preset_weight = {x.source: x.weight for x in e.transition.in_arcs}
        postset_weight = {x.target: x.weight for x in e.transition.out_arcs}

        for c in pre:
            petri_utils.add_arc_from_to(c, e, res)
            p = c.place
            dm = c.markers - preset_weight.get(p, 0) + postset_weight.get(p, 0)
            c = NSafeCondition(p, dm)
            res.add_condition(c)
            petri_utils.add_arc_from_to(e, c, res)

        co.update(e, res.places)
        config = settings.config(e)
        m = config.mark()
        if m not in min_by_mark or settings.cmp_events(min_by_mark[m], e) >= 0:
            update_possible_extensions(pe, e, net.transitions, co)
            min_by_mark[m] = e

    for a in bot.out_arcs:
        a.target.in_arcs.remove(a)
        res.arcs.remove(a)

    res.transitions.remove(bot)

    return res
