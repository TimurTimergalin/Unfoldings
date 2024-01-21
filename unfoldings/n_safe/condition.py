from obj import Condition


class NSafeCondition(Condition):
    def __init__(self, place, markers):
        super().__init__(place)
        self.markers = markers

    def __repr__(self):
        return f"<{self.name} of {self.place.name} with {self.markers} markers>"
