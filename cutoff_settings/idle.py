from .abstract import CutoffSettings


class IdleCutoffSettings(CutoffSettings):
    r"""Класс настроек, при которых никакое событие не будет отсечено. Это соответствует C_e = \emptyset"""
    def check_cutoff(self, event, order_settings):
        return False, {}

    def update(self, event, order_settings, *, mark=None, **kwargs):
        pass
