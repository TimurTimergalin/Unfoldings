from itertools import zip_longest, chain

from pm4py.objects.petri_net.obj import Marking, PetriNet
from pm4py.objects.petri_net.utils import petri_utils

from .event import NSafeEvent


# Проверка на то, что событие, помеченное переходом t, может иметь в качестве preset-а
# co-set с разметкой m
def is_enabled(t, m):
    pre_set = {x.source: x.weight for x in t.in_arcs}
    post_set = {x.target for x in t.out_arcs}
    for p, k in zip_longest(set(pre_set) | post_set, m):
        # Такое возможно, только если количество ключей не совпадает
        if p is None or k is None:
            return False

        if k not in pre_set and k not in post_set:
            return False

        if p in pre_set and m[p] < pre_set[p]:
            return False

    return True


# Обновление очереди потенциальных событий после добавления нового события
# pe - очередь
# new - добавленное событие
# transitions - множество всех переходов в изначальной сети
# co - отношение конкурентности
def update_possible_extensions(pe, new, c, co, transitions=None):
    # for co_set in co.new_co_sets(new):
    #     m = Marking({x.place: x.markers for x in co_set})
    #     for t in transitions:
    #         if is_enabled(t, m):
    #             e = NSafeEvent(t, m)
    #
    #             for c in co_set:
    #                 arc = PetriNet.Arc(c, e)
    #                 e.in_arcs.add(arc)
    #             pe.add((e, co_set))
    t = new.transition
    transitions = transitions or set(
        chain.from_iterable(
            petri_utils.post_set(x) | petri_utils.pre_set(x)
            for x in petri_utils.post_set(t) | petri_utils.pre_set(t)
        )
    )

    new_postset = petri_utils.post_set(new)
    for t in transitions:
        preset = petri_utils.pre_set(t)
        postset = petri_utils.post_set(t)
        n = len(preset | postset)
        preset_weight = {x.source: x.weight for x in t.in_arcs}
        preset_conds = [x for x in new_postset if x.place in postset and x.place not in preset or x.place in preset and x.markers >= preset_weight[x.place]]
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

