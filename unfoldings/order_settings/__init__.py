"""
В этом модуле представлены реализации настроек порядка - классов, задача которых - генерировать локальные конфигурации
событий и определять адекватный порядок на конфигурациях.

В модуле представлены следующие настройки:
1. Idle - все конфигурации считаются несравнимыми
2. basic - конфигурации представляются обычным множеством и сравниваются по длинам
(базовый алгоритм МакМиллана)
3. foata - конфигурации представляются списком "слоев", соответствующих Фоатовской нормальной форме, и сравниваются
по отсортированным меткам (TotalOrderSettings) или по Фоатовской нормальной форме (FoataOrderSettigs)
4. abstract - интерфейс конфигураций и настроек порядка для новых реализаций

Все встроенные настройки порядка (кроме idle) включаются сравнение длин конфигураций, поэтому длины конфигураций
при использовании этих настроек событий кэшируются
"""

from .abstract import OrderSettings, Configuration
from .basic import BasicOrderSettings
from .foata import FoataOrderSettings, TotalOrderSettings
from .idle import IdleOrderSettings

__all__ = [
    "BasicOrderSettings",
    "FoataOrderSettings",
    "TotalOrderSettings",
    "OrderSettings",
    "Configuration",
    "IdleOrderSettings"
]