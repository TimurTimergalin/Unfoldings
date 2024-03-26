from .abstract import Decorations
from .idle import IdleDecorations


class LabelsDecorations(Decorations):
    """Декорации, позволяющие изменять надписи на элементах сети"""
    def __init__(self, inner=None, /, *, conditions, events):
        """
        :param inner: внутренняя декорация, по умолчанию idle
        :param conditions: функция, возвращающая надпись на условии
        :param events: функция, возвращающая надпись на событии
        """
        self.events = events
        self.inner = inner or IdleDecorations()
        self.conditions = conditions

    @classmethod
    def standard(cls, inner=None, /):
        """
        Базовые декорации для стандартного алгоритма. Надписи условий и событий будут совпадать с именами позиций и
        переходов, которыми они помечены
        :param inner: внутренняя декорация, по умолчанию idle
        :return:
        """
        return LabelsDecorations(inner,
                                 conditions=lambda c: c.place.name,
                                 events=lambda e: e.transition.name if e.transition is not None else ""
                                 )

    @classmethod
    def n_safe(cls, inner=None, /):
        """
        Базовые декорации для n-safe алгоритма. Надписи условий будут иметь вид "{name}:{markers}", где name -
        имя позиции начальной сети, которой помечено условие, markers - количество маркеров в этой позиции, которому
        соответствует условию.
        Аналогично, надписи событий будут иметь вид: "{name}{marking}"
        :param inner:
        :return:
        """
        return LabelsDecorations(inner,
                                 conditions=lambda c: f"{c.place.name}:{c.markers}",
                                 events=lambda e: (f"{e.transition.name}"
                                                   f"{dict((k.name, v) for k, v in e.marking.items())
                                                   if e.marking is not None and e.transition is not None else ''}")
                                 )

    def add_condition(self, c):
        self.inner.add_condition(c)
        self.inner.get()[c]["label"] = self.conditions(c)

    def add_event(self, e):
        self.inner.add_event(e)
        self.inner.get()[e]["label"] = self.events(e)

    def get(self):
        return self.inner.get()
