from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils


# Класс, представляющий условие в префиксе
class Condition(PetriNet.Place):
    def __init__(self, place):
        super().__init__("")  # Название он получит при добавлении в префикс (см. obj/prefix.py)
        self.place = place  # Позиция в сети, соответствующая данному условию

    # Единственное событие в preset-е
    @property
    def input_event(self):
        e, = petri_utils.pre_set(self)  # По определению развертки, preset условия состоит из одного события
        return e
