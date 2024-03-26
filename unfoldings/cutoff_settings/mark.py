from .abstract import CutoffSettings


class MarkCutoffSettings(CutoffSettings):
    """Класс настроек, при которых для нахождения отсечек сравнивается разметка локальных конфигураций"""

    def __init__(self):
        self.min_by_mark = {}

    def check_cutoff(self, event, order_settings):
        config = order_settings.conf(event)
        m = config.mark()

        return m in self.min_by_mark and order_settings.cmp_events(self.min_by_mark[m], event, config2=config) < 0, {
            "mark": m}

    def update(self, event, order_settings, *, mark=None, **kwargs):
        if mark is None:
            mark = order_settings(event)

        self.min_by_mark[mark] = event
