from abc import ABC, abstractmethod


class CutoffSettings(ABC):
    """Интерфейс настроек отсечения"""

    @abstractmethod
    def check_cutoff(self, event, order_settings):
        """
        Проверка, является ли событие отсечкой
        :param event: проверяемое событие
        :param order_settings: настройки порядка
        :return: кортеж (res, hint), где res - результат проверки (True/False), hint - словарь "подсказок" - значений,
        которые будут переданы как аргументы в CutoffSettings.update. Подсказки нужны для оптимизации - зачастую в
        check_cutoff и update производятся схожие вычисления
        """

    @abstractmethod
    def update(self, event, order_settings, **kwargs):
        """
        Обновление объекта настроек при добавлении нового события
        :param event: новое событие
        :param order_settings: настройки порядка
        :param kwargs: "подсказки" для ускорения вычислений. Сюда передаются подсказки из метода check_cutoff
        """
