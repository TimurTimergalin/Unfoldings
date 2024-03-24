from .abstract import Decorations
from .idle import IdleDecorations


class LabelsDecorations(Decorations):
    def __init__(self, inner=None, /, *, conditions, events):
        self.events = events
        self.inner = inner or IdleDecorations()
        self.conditions = conditions

    @classmethod
    def standard(cls, inner=None, /):
        return LabelsDecorations(inner,
                                 conditions=lambda c: c.place.name,
                                 events=lambda e: e.transition.name if e.transition is not None else ""
                                 )

    @classmethod
    def n_safe(cls, inner=None, /):
        return LabelsDecorations(inner,
                                 conditions=lambda c: f"{c.place.name}:{c.markers}",
                                 events=lambda e: (f"{e.transition.name}"
                                                   f"[{dict((k.name, v) for k, v in e.marking.items())
                                                   if e.marking is not None and e.transition is not None else ''}]")
                                 )

    def add_condition(self, c):
        self.inner.add_condition(c)
        self.inner.get()[c]["label"] = self.conditions(c)

    def add_event(self, e):
        self.inner.add_event(e)
        self.inner.get()[e]["label"] = self.events(e)

    def get(self):
        return self.inner.get()
