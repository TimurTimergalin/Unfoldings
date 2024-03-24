from .abstract import OrderSettings


class IdleOrderSettings(OrderSettings):
    def config(self):
        return None

    def cmp_events(self, *args, **kwargs):
        return 0
