from obj import Event


# Отличие от обычных событий в том, что теперь они помечены не только переходом в изначальной сети,
# но и разметкой preset-а
class NSafeEvent(Event):
    def __init__(self, transition, marking):
        super().__init__(transition)
        self.marking = marking

        if transition is not None:
            self.label = (f"{transition.name}"
                          f"[{dict((k.name, v) for k, v in marking.items()) if marking is not None else ''}]")

    def __repr__(self):
        t_name = r"\bot" if self.transition is None else self.transition.name
        return f"<{self.name} of {t_name} at {self.marking}>"
