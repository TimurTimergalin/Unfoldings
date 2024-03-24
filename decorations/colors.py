from .abstract import Decorations
from .idle import IdleDecorations


class ColorsDecorations(Decorations):
    def __init__(self, inner=None, /, *, conditions=None, events=None, starting_conditions=None, cutoff_events=None):
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
