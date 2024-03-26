from pm4py.objects.petri_net.obj import Marking
from pm4py.objects.petri_net.utils import petri_utils

from ...obj import Event


# Отличие от обычных событий в том, что теперь они помечены не только переходом в изначальной сети,
# но и разметкой preset-а
class NSafeEvent(Event):
    def __init__(self, transition, marking):
        super().__init__(transition)
        self.marking = marking

    def __repr__(self):
        t_name = r"\bot" if self.transition is None else self.transition.name
        return f"<{self.name} of {t_name} at {self.marking}>"

    @property
    def net_label(self):
        return super().net_label, hash(self.marking)

    def postset_marking(self):
        return Marking({c.place: c.markers for c in petri_utils.post_set(self)})

    def preset_marking(self):
        return Marking({c.place: c.markers for c in petri_utils.pre_set(self)})
