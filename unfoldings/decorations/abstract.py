from abc import ABC, abstractmethod


class Decorations(ABC):
    """Интерфейс декораций"""

    def add_event(self, e):
        """
        Вызывается, когда событие (отсеченное или нет) добавляется в сеть
        :param e: добавленное событие
        """

    def add_cutoff_event(self, e):
        """
        Вызывается, когда событие помечается как событие-отсечка. Этот метод вызывается после add_event
        :param e: событие-отсечка
        """

    def add_condition(self, c):
        """
        Вызывается, когда условие добавляется в сеть
        :param c: добавленное условие
        """

    def add_starting_condition(self, c):
        """
        Вызывается, когда в сеть добавляют начальное условие. Этот метод вызывается после add_condition
        :param c: стартовое условие
        """

    @abstractmethod
    def get(self):
        """
        Метод для получения словаря полученных декораций, который затем можно передать в pm4py.view_petri_net
        :return: словарь декораций
        """
        pass
