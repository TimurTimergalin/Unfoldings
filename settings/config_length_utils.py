class ConfigLength:
    def __init__(self, config_type):
        self.cache = {}
        self.conf = config_type

    def calculated(self, ev):
        return ev in self.cache

    def save(self, ev, length):
        self.cache[ev] = length

    def __call__(self, ev):
        return self.cache.get(ev, len(self.conf(ev)))