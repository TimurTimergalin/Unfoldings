from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils


class Condition(PetriNet.Place):
    """
    Класс, представляющий условие развертки
    :attribute place: позиция изначальной сети, которой помечено условие
    """
    def __init__(self, place):
        super().__init__("")  # Название он получит при добавлении в префикс (см. obj/prefix.py)
        self.place = place  # Позиция в сети, соответствующая данному условию

    # Единственное событие в preset-е
    @property
    def input_event(self):
        e, = petri_utils.pre_set(self)  # По определению развертки, preset условия состоит из одного события
        return e

    def __repr__(self):
        return f"<{self.name} of {self.place.name}>"

    @property
    def net_label(self):
        return id(self.place)
