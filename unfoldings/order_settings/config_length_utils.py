class ConfigLength:
    """Класс для кэширования длин локальных конфигураций событий"""

    def __init__(self, config_type):
        self.cache = {}
        self.conf = config_type

    def calculated(self, ev):
        return ev in self.cache

    def save(self, ev, length):
        self.cache[ev] = length

    def __call__(self, ev):
        res = self.cache.get(ev, len(self.conf(ev)))
        self.save(ev, res)
        return res
