from abc import ABC, abstractmethod


class CutoffSettings(ABC):
    @abstractmethod
    def check_cutoff(self, event, order_settings):
        pass

    @abstractmethod
    def update(self, event, order_settings, *, mark=None, **kwargs):
        pass
