from pm4py.objects.petri_net.utils import petri_utils

from itertools import product


# Класс, представляющий отношение co(x, y) := not (x <= y) and not "x в конфликте с y"
class Co:
    def __init__(self):
        self.pairs = set()  # Отношение представляется в виде множества пар

    def __call__(self, f, s):
        return (f, s) in self.pairs

    # Обновляет отношение после добавления нового события
    # new_event - новое событие
    # conditions - множество всех условий в префиксе (в том числе новых)
    def update(self, new_event, conditions):
        new = petri_utils.post_set(new_event)  # post_set нового события
        old = conditions - new  # Все остальные условия

        concurrent_with = set()  # Старые условия, с которыми конкурентны все условия из preset-а нового события

        for c in old:
            for c1 in petri_utils.pre_set(new_event):
                if not self(c, c1) or c == c1:
                    break
            else:  # Если c конкурентно со всеми условиями из preset-а нового события
                concurrent_with.add(c)

        self.pairs.update((x, y) for x, y in product(new, new))
        self.pairs.update((x, y) for x, y in product(new, concurrent_with))
        self.pairs.update((x, y) for x, y in product(concurrent_with, new))

    # Перечисляет все co-set-ы, которые появились в результате добавления нового события в префикс
    # (co-set - любое множество попарно-конкурентных условий)
    # new - новое событие
    def new_co_sets(self, new):
        new_post_set = petri_utils.post_set(new)
        # Пары из отношения сортируются так, чтобы все пары с одинаковым первым элементом шли подряд, и
        # при этом сначала шли те пары, у которых первый элемент - новое условие
        sorted_co = sorted(self.pairs, key=lambda x: (x[0] not in new_post_set, id(x[0])))
        return self._co_sets(sorted_co, new_post_set)

    # Рекурсивно перечисляет все новые co-set-ы (см. Co.new_co_sets)
    # sorted_co - отсортированное отношение co
    # new - множество новых условий
    # allowed - элементы, которые можно добавить в текущий coset
    # constructed - текущий coset
    # current - индекс в sorted_co
    def _co_sets(self, sorted_co, new, allowed=None, constructed=None, current=0):
        if constructed is None:
            constructed = set()
        n = len(sorted_co)
        if current >= n:  # sorted_co закончился
            return
        if allowed is None and sorted_co[current][0] not in new:  # Ни одно из новых значений не добавлено
            # Значит все coset-ы в этой ветви уже учтены в pe
            return

        # Пропуск недопустимых значений
        if allowed is not None:
            while current < n and sorted_co[current][0] not in allowed:
                current += 1

        if current >= n:  # sorted_co закончился
            return

        # el - условие, которое можно добавить в текущий coset
        el = sorted_co[current][0]

        # Конструирование множества всех таких x, что el co x
        new_allowed = set()
        while current < n and (pair := sorted_co[current])[0] == el:
            new_allowed.add(pair[1])
            current += 1

        # текущий coset в случае добавления el
        new_constructed = constructed | {el}
        yield new_constructed
        # Ветвь, где el добавлен
        yield from self._co_sets(sorted_co, new, new_allowed & allowed if allowed is not None else new_allowed,
                                 new_constructed,
                                 current)
        # Ветвь, где el пропущен
        yield from self._co_sets(sorted_co, new, allowed, constructed, current)

    def __repr__(self):
        return repr(self.pairs)
