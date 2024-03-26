# Реализация очереди с приоритетом.
# Используется для нахождения возможного расширения с наименьшей локальной конфигурацией.
# В очереди будут лежать пары (event, preset), где event - возможное расширение, preset - условия, которые
# будут составлять его preset.
class PriorityQueue:
    """
    Реализация очереди с приоритетом.
    Используется для нахождения возможного расширения с наименьшей локальной конфигурацией.
    В очереди будут лежать пары (event, preset), где event - возможное расширение, preset - условия, которые
    будут составлять его preset.
    """
    def __init__(self, events_cmp):  # event_cmp - функция сравнения событий
        self.cmp = events_cmp
        self.heap = []

    @staticmethod
    def _left_child(ind):
        return 2 * ind + 1

    @staticmethod
    def _right_child(ind):
        return 2 * ind + 2

    @staticmethod
    def _parent(ind):
        return (ind - 1) // 2

    def _in_bounds(self, ind):
        return 0 <= ind < len(self.heap)

    def _heapify_down(self, ind):
        if not self._in_bounds(ind):
            return
        while True:
            li = self._left_child(ind)
            ri = self._right_child(ind)

            lv = self.heap[li][0] if self._in_bounds(li) else None
            rv = self.heap[ri][0] if self._in_bounds(ri) else None
            cv = self.heap[ind][0]

            if lv is not None and self.cmp(cv, lv) > 0 and (rv is None or self.cmp(rv, lv) >= 0):
                self.heap[ind], self.heap[li] = self.heap[li], self.heap[ind]
                ind = li
            elif rv is not None and self.cmp(cv, rv) > 0 and (lv is None or self.cmp(lv, rv) >= 0):
                self.heap[ind], self.heap[ri] = self.heap[ri], self.heap[ind]
                ind = ri
            else:
                break

    def _heapify_up(self, ind):
        if not self._in_bounds(ind):
            return
        while True:
            pi = self._parent(ind)
            if not self._in_bounds(pi):
                break

            pv = self.heap[pi][0]
            cv = self.heap[ind][0]

            if self.cmp(cv, pv) < 0:
                self.heap[ind], self.heap[pi] = self.heap[pi], self.heap[ind]
                ind = pi
            else:
                break

    def add(self, el):  # Добавить новое потенциальное событие
        ni = len(self.heap)
        self.heap.append(el)
        self._heapify_up(ni)

    def pop(self):  # Извлечь потенциальное событие с минимальной локальной конфигурацией
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]

        r = self.heap.pop()
        self._heapify_down(0)
        return r

    def __len__(self):
        return len(self.heap)

    def __repr__(self):
        return repr(self.heap)
