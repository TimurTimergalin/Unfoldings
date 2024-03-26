from itertools import product

from pm4py.objects.petri_net.utils import petri_utils


class Co:
    """
    Класс, представляющий отношение co(x, y) := [not (x <= y) and not (x # y)] на условиях сети
    """

    def __init__(self):
        self.pairs = set()  # Отношение представляется в виде множества пар

    def __call__(self, f, s):
        """Определяет, конкурентны ли условия"""
        return (f, s) in self.pairs or (s, f) in self.pairs

    def update(self, new_event, conditions):
        """
        Обновляет отношение после добавления нового события
        :param new_event: новое событие
        :param conditions: множество всех условий в префиксе (в том числе новых)
        """
        new = petri_utils.post_set(new_event)  # post_set нового события
        old = conditions - new  # Все остальные условия

        concurrent_with = []  # Старые условия, с которыми конкурентны все условия из preset-а нового события
        # (а значит и само новое событие)

        for c in old:
            for c1 in petri_utils.pre_set(new_event):
                if not self(c, c1) or c == c1:
                    break
            else:  # Если `c` конкурентно со всеми условиями из preset-а нового события
                concurrent_with.append(c)

        self.pairs.update((x, y) for x, y in product(new, new) if x != y)
        self.pairs.update((x, y) for x, y in product(new, concurrent_with))

        return concurrent_with

    def __repr__(self):
        return repr(self.pairs)
