from .abstract import CutoffSettings


class IdleCutoffSettings(CutoffSettings):
    def check_cutoff(self, event, order_settings):
        return False, {}

    def update(self, event, order_settings, *, mark=None, **kwargs):
        pass
