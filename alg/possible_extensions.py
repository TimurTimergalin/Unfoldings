from pm4py.objects.petri_net.obj import Marking, PetriNet
from pm4py.objects.petri_net.utils import petri_utils

from itertools import chain, product, combinations
from collections import defaultdict

from obj import Event


# Обновление очереди потенциальных событий после добавления нового события
# pe - очередь
# new - добавленное событие
# transitions - множество всех переходов в изначальной сети
# co - отношение конкурентности
def update_possible_extensions(pe, new, c, co, transitions=None):
    t = new.transition
    transitions = transitions or set(
        chain.from_iterable(
            petri_utils.post_set(x)
            for x in petri_utils.post_set(t)
        )
    )

    new_postset = petri_utils.post_set(new)
    for t in transitions:
        n = sum(x.weight for x in t.in_arcs)
        preset = petri_utils.pre_set(t)
        preset_marking = Marking(x.source for x in t.in_arcs for _ in range(x.weight))

        preset_by_place = defaultdict(lambda: [])
        for x in new_postset:
            if x.place in preset:
                preset_by_place[x.place].append(x)
        for cond in c:
            if cond.place in preset_by_place and cond not in new_postset:  # Второе условие нужно только при добавлении \bot
                preset_by_place[cond.place].append(cond)

        for choice in product(*(list(combinations(preset_by_place[cond], preset_marking[cond])) for cond in preset_by_place)):
            preset_conds = list(chain.from_iterable(choice))

            for cond in preset_conds:
                if cond in new_postset:
                    break
            else:  # Если в выбранном coset-е нет новых элементов
                continue  # то это расширение уже добавлено (если нужно)

            cover(pe, t, preset_conds, co, c, preset_marking, n)

        # preset_conds = list(filter(lambda x: x.place in preset, petri_utils.post_set(new)))
        # cover(pe, t, preset_conds, co, c, preset_marking, n)


def cover(pe, t, preset_conds, co, c, preset_marking, n):
    if len(preset_conds) == n:
        e = Event(t)
        for c in preset_conds:
            arc = PetriNet.Arc(c, e)
            e.in_arcs.add(arc)
        pe.add((e, set(preset_conds)))
    else:
        left = set(preset_marking) - set(x.place for x in preset_conds)
        p = next(iter(left))

        possible_additions = [x for x in c if x.place == p]
        for choice in combinations(possible_additions, preset_marking[p]):
            new_c = [x for x in c if x not in choice and all(co(d, x) for d in choice)]
            preset_conds.extend(choice)
            cover(pe, t, preset_conds, co, new_c, preset_marking, n)

            for _ in range(preset_marking[p]):
                preset_conds.pop()

        # for d in filter(lambda x: x.place == p, c):
        #     new_c = list(filter(lambda x: co(d, x) and x != d, c))
        #     preset_conds.append(d)
        #     cover(pe, t, preset_conds, co, new_c, preset_marking, n)
        #     preset_conds.pop()
