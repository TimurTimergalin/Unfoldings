from abc import ABC, abstractmethod

from pm4py.objects.petri_net.obj import Marking


class OrderSettings(ABC):
    """Интерфейс настроек"""

    @abstractmethod
    def config(self, event):
        """
        Генерирует локальную конфигурацию события
        :param event: событие
        :return: локальную конфигурацию event
        """

    @abstractmethod
    def cmp_events(self, e1, e2, **kwargs):
        """
        Сравнивает события
        :param e1: первое событие
        :param e2: второе событие
        :param kwargs: "подсказки", ускоряющие вычисления. Каждый класс настроек может принимать различные "подсказки"
        :return: отрицательное число, если e1 < e1; положительное число, если e1 > e2; 0 в других случаях
        """


# Скопированная реализация collections.Counter._keep_positive (это внутренний метод, который может исчезнуть
# в последующих версиях python)
def _keep_positive(counter):
    nonpositive = [elem for elem, count in counter.items() if not count > 0]
    for elem in nonpositive:
        del counter[elem]
    return counter


class Configuration(ABC):
    """Абстрактный класс конфигурации"""

    @abstractmethod
    def __iter__(self):
        """Перечисляет все события в конфигурации"""

    @abstractmethod
    def __len__(self):
        """Количество событий в конфигурации"""

    def mark(self):
        """
        Вычисляет разметку среза конфигурации
        :return: нужную разметку
        """
        res = Marking()
        for e in self:
            post_set_marking = e.postset_marking()
            pre_set_marking = e.preset_marking()

            res.update(post_set_marking)
            res.subtract(pre_set_marking)

        return _keep_positive(res)
