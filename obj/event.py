from pm4py.objects.petri_net.obj import PetriNet


# Класс, представляющий событие в префиксе
class Event(PetriNet.Transition):
    def __init__(self, transition):  # None, если event = \bot
        # Название он получит при добавлении в префикс (см. obj/prefix.py)
        super().__init__("", label=transition.name if transition is not None else "")
        self.transition = transition  # Переход в сети, соответствующий данному событию

    def __repr__(self):
        bot = r'\bot'
        return f"<{self.name} of {self.transition.name if self.transition else bot}>"
