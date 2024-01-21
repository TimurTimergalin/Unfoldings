from obj import Prefix


class NSafePrefix(Prefix):
    def condition_label(self, c):
        return f"{c.place.name}:{c.markers}"
