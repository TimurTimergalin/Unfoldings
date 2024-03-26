from .abstract import Decorations
from collections import defaultdict


class IdleDecorations(Decorations):
    """Пустые декорации"""
    def __init__(self):
        self.decorations = defaultdict(lambda: {})

    def get(self):
        return self.decorations
