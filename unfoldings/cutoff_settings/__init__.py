r"""
В это м модуле представлены реализации настроек отсечения - классов, задача которых - выбирать, с каким конфигурациями
развертки будет сравниваться локальная конфигурация потенциального события-отсечки (это соответствует \approx и
\{C_e\}_{e \in E} в контексте срезания)

В модуле представлены следующие настройки:
1. idle - никакие события не будут отсечками
2. mark - соответствует \approx(c, c') := Mark(c) = Mark(c') и C_e = C_{loc}
3. abstract - интерфейс настроек для новых реализаций
"""
from .abstract import CutoffSettings
from .idle import IdleCutoffSettings
from .mark import MarkCutoffSettings

__all__ = [
    "CutoffSettings",
    "MarkCutoffSettings",
    "IdleCutoffSettings"
]
