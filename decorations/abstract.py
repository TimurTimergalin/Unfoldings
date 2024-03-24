from abc import ABC, abstractmethod


class Decorations(ABC):
    def add_event(self, e):
        pass

    def add_cutoff_event(self, e):
        pass

    def add_condition(self, c):
        pass

    def add_starting_condition(self, c):
        pass

    @abstractmethod
    def get(self):
        pass
