from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils


# Класс, представляющий событие в префиксе
class Event(PetriNet.Transition):
    def __init__(self, transition):  # None, если event = \bot
        # Название он получит при добавлении в префикс (см. obj/prefix.py)
        super().__init__("", "")
        self.transition = transition  # Переход в сети, соответствующий данному событию

    def __repr__(self):
        bot = r'\bot'
        return f"<{self.name} of {self.transition.name if self.transition else bot}>"

    @property
    def net_label(self):
        return id(self.transition)

    def postset_marking(self):
        return Marking(c.place for c in petri_utils.post_set(self))

    def preset_marking(self):
        return Marking(c.place for c in petri_utils.pre_set(self))
