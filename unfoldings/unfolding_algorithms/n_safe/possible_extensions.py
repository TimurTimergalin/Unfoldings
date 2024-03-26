from itertools import chain

from pm4py.objects.petri_net.obj import Marking, PetriNet
from pm4py.objects.petri_net.utils import petri_utils

from .event import NSafeEvent


def update_possible_extensions(pe, new, c, co):
    """
    Обновление очереди возможных расширений после добавления нового события
    :param pe: очередь возможных расширений
    :param new: добавленное событие
    :param c: множество условий, конкурентных с new (считается в Co.update)
    :param co: отношение конкурентности
    """
    transitions = set(
        chain.from_iterable(
            petri_utils.post_set(x) | petri_utils.pre_set(x)
            for x in (y.place for y in petri_utils.post_set(new))
        )
    )

    new_postset = petri_utils.post_set(new)
    for t in transitions:
        preset = petri_utils.pre_set(t)
        postset = petri_utils.post_set(t)
        n = len(preset | postset)
        preset_weight = {x.source: x.weight for x in t.in_arcs}
        preset_conds = [x for x in new_postset if
                        x.place in postset and x.place not in preset or x.place in preset and x.markers >=
                        preset_weight[x.place]]
        cover(pe, t, preset_conds, co, c, preset, postset, preset_weight, n)


def cover(pe, t, preset_conds, co, c, preset, postset, preset_weight, n):
    if len(preset_conds) == n:
        e = NSafeEvent(t, Marking({x.place: x.markers for x in preset_conds}))
        for c in preset_conds:
            arc = PetriNet.Arc(c, e)
            e.in_arcs.add(arc)
        pe.add((e, set(preset_conds)))
    else:
        left = preset - set(x.place for x in preset_conds)
        if left:
            p = next(iter(left))
            choose_from = (x for x in c if x.place == p and x.markers >= preset_weight[p])
        else:
            left = postset - set(x.place for x in preset_conds)
            p = next(iter(left))
            choose_from = (x for x in c if x.place == p)

        for d in choose_from:
            new_c = [x for x in c if co(d, x) and x != d]
            preset_conds.append(d)
            cover(pe, t, preset_conds, co, new_c, preset, postset, preset_weight, n)
            preset_conds.pop()
