from itertools import zip_longest

from pm4py.objects.petri_net.obj import Marking, PetriNet

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
def update_possible_extensions(pe, new, transitions, co):
    for co_set in co.new_co_sets(new):
        m = Marking({x.place: x.markers for x in co_set})
        for t in transitions:
            if is_enabled(t, m):
                e = NSafeEvent(t, m)

                for c in co_set:
                    arc = PetriNet.Arc(c, e)
                    e.in_arcs.add(arc)
                pe.add((e, co_set))
