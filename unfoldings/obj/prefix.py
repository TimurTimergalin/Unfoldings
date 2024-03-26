from pm4py.objects.petri_net.obj import PetriNet


# Класс, представляющий префикс развёртки
class Prefix(PetriNet):
    """
    Класс, представляющий префикс развертки
    :attribute finished: закончилось ли построения префикса или нет (нет в случае, если при построении было поставлено
    ограничение на количество событий, которое было превышено)
    :attribute cutoff_events: множество событий-отсечек
    """

    def __init__(self, net_name):
        super().__init__(f"Finite complete prefix of '{net_name}'")
        # Счётчики событий и условий для наименования
        self.event_counter = 0
        self.condition_counter = 1
        self.cutoff_events = set()
        self.finished = False

    def add_condition(self, c):
        c.name = f"c{self.condition_counter}"
        self.condition_counter += 1
        self.places.add(c)

    def add_event(self, e):
        e.name = f"e{self.event_counter}"
        self.event_counter += 1
        self.transitions.add(e)

    def add_cutoff(self, ev):
        self.cutoff_events.add(ev)
