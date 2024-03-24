import pm4py
from pm4py.objects.petri_net.obj import PetriNet
from collections import defaultdict


# Класс, представляющий префикс развёртки
class Prefix(PetriNet):
    def __init__(self, net_name):
        super().__init__(f"Finite complete prefix of '{net_name}'")
        self.decorations = defaultdict(lambda: {})  # decorations для pm4py.view_petri_net
        # Счётчики событий и условий для наименования
        self.event_counter = 0
        self.condition_counter = 1
        self.cutoff_events = set()
        self.finished = False

    def add_condition(self, c):
        c.name = f"c{self.condition_counter}"
        self.condition_counter += 1
        self.places.add(c)
        self.decorations[c]["label"] = self.condition_label(c)

    def condition_label(self, c):
        return c.place.name

    def add_event(self, e):
        e.name = f"e{self.event_counter}"
        self.event_counter += 1
        self.transitions.add(e)

    def add_cutoff(self, ev):
        self.cutoff_events.add(ev)
        self.decorations[ev]["color"] = "#ffaaaa"

    def add_starting_condition(self, c):
        self.decorations[c]["color"] = "#aaffaa"

    def view(self):
        pm4py.view_petri_net(self, None, None, decorations=self.decorations)
