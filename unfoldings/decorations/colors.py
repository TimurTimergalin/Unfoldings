from .abstract import Decorations
from .idle import IdleDecorations


class ColorsDecorations(Decorations):
    """Декорации, позволяющие менять цвет элементов сети"""

    def __init__(self, inner=None, /, *, conditions="#ffffff", events="#ffffff", starting_conditions=None, cutoff_events=None):
        """
        :param inner: внутренняя декорация, по умолчанию idle
        :param conditions: цвет условий, по умолчанию на выбор pm4py
        :param events: цвет событий, по умолчанию на выбор pm4py
        :param starting_conditions: цвет начальных событий, по умолчанию совпадает с conditions
        :param cutoff_events: цвет отсеченных событий, по умолчанию совпадает с events
        """
        self.events = events
        self.starting_conditions = starting_conditions
        self.cutoff_events = cutoff_events
        self.conditions = conditions
        self.inner = inner or IdleDecorations()

    def add_event(self, e):
        self.inner.add_event(e)
        if self.events is not None:
            self.inner.get()[e]["color"] = self.events

    def add_cutoff_event(self, e):
        self.inner.add_cutoff_event(e)
        if self.cutoff_events is not None:
            self.inner.get()[e]["color"] = self.cutoff_events

    def add_condition(self, c):
        self.inner.add_condition(c)
        if self.conditions is not None:
            self.inner.get()[c]["color"] = self.conditions

    def add_starting_condition(self, c):
        self.inner.add_starting_condition(c)
        if self.starting_conditions is not None:
            self.inner.get()[c]["color"] = self.starting_conditions

    def get(self):
        return self.inner.get()
