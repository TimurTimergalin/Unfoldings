from ...obj import Condition


# Отличие от обычных условий в том, что теперь они помечены не только позицией из начальной сети,
# но и количеством маркеров в этой позиции
class NSafeCondition(Condition):
    def __init__(self, place, markers):
        super().__init__(place)
        self.markers = markers

    def __repr__(self):
        return f"<{self.name} of {self.place.name} with {self.markers} markers>"

    @property
    def net_label(self):
        return super().net_label, self.markers
