from collections import defaultdict

from .abstract import Decorations


class IdleDecorations(Decorations):
    """Пустые декорации"""

    def __init__(self):
        self.decorations = defaultdict(lambda: {})

    def get(self):
        return self.decorations
