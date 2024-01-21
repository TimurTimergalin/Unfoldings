import pm4py
from pm4py.objects.petri_net.obj import PetriNet


# Класс, представляющий префикс развёртки
class Prefix(PetriNet):
    def __init__(self, net_name):
        super().__init__(f"Finite complete prefix of '{net_name}'")
        self.condition_labels = {}  # Пометки для условий (в pm4py встроенные label-ы для позиций не предусмотрены)
        # Счётчики событий и условий для наименования
        self.event_counter = 0
        self.condition_counter = 1

    def add_condition(self, c):
        c.name = f"c{self.condition_counter}"
        self.condition_counter += 1
        self.places.add(c)
        self.condition_labels[c] = {"label": self.condition_label(c)}

    def condition_label(self, c):
        return c.place.name

    def add_event(self, e):
        e.name = f"e{self.event_counter}"
        self.event_counter += 1
        self.transitions.add(e)

    def view(self):
        pm4py.view_petri_net(self, None, None, decorations=self.condition_labels)
