from pm4py.objects.petri_net.obj import Marking

from itertools import zip_longest

from obj import Event


# Проверка на то, что preset-у события соответствует разметка
def is_enabled(t, m):
    for a, k in zip_longest(t.in_arcs, m):
        # Такое возможно, только если количество ключей не совпадает (а значит и словари тоже)
        if a is None or k is None:
            return False

        if m[a.source] != a.weight:
            return False

    return True


# Обновление очереди потенциальных событий после добавления нового события
# pe - очередь
# new - добавленное событие
# transitions - множество всех переходов в изначальной сети
# co - отношение конкурентности
# event_factory - метод создания новых событий
def update_possible_extensions(pe, new, transitions, co):
    for co_set in co.new_co_sets(new):
        m = Marking(x.place for x in co_set)
        for t in transitions:
            if is_enabled(t, m):
                pe.append((Event(t), co_set))
