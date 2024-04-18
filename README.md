# ИССЛЕДОВАНИЕ И ЭКСПЕРИМЕНТАЛЬНАЯ РЕАЛИЗАЦИЯ АЛГОРИТМА ПОСТРОЕНИЯ РАЗВЕРТОК ДЛЯ МОДЕЛЕЙ ПРОЦЕССОВ В ВИДЕ СЕТЕЙ ПЕТРИ
Данный репозиторий содержит исходный код, написанный в рамках курсовой работы на данную тему.

## Структура проекта

```
│   LICENSE
│   README.md
|   example.py
├───nets_generators
│   │   dining_philosophers.py
│   │   dining_philosophers_with_dict.py
│   │   generate_slotted_ring.py
│   │   milners_cyclic_scheduler.py
│   │   mutual_exclusion.py
│   │   __init__.py
└───unfoldings
    │   __init__.py
    ├───alg
    │   │   concurrency_relation.py
    │   │   possible_extensions.py
    │   │   priority_queue.py
    │   │   __init__.py
    ├───cutoff_settings
    │   │   abstract.py
    │   │   idle.py
    │   │   mark.py
    │   │   __init__.py
    ├───decorations
    │   │   abstract.py
    │   │   colors.py
    │   │   idle.py
    │   │   labels.py
    │   │   __init__.py
    ├───obj
    │   │   condition.py
    │   │   event.py
    │   │   prefix.py
    │   │   __init__.py
    ├───order_settings
    │   │   abstract.py
    │   │   basic.py
    │   │   config_length_utils.py
    │   │   foata.py
    │   │   idle.py
    │   │   __init__.py
    ├───unfolding_algorithms
    │   │   standard.py
    │   │   __init__.py
    │   ├───n_safe
    │   │   │   build_prefix.py
    │   │   │   condition.py
    │   │   │   event.py
    │   │   │   possible_extensions.py
    │   │   │   __init__.py
```

Папка `nets_generator` содержит скрипты для генерации сетей Петри, использовавшихся при экспериментальной оценке программ.

Исходный код проекта лежит в папке `unfoldings` и содержит следующие разделы:

1. `alg` содержит в себе исходный код различных вспомогательных алгоритмов;
2. `cutoff_settings` содержит в себе определение интерфейса настроек отсечения и его реализаций;
3. `decorations` содержит в себе определение интерфейс декораций - настроек вывода префикса;
4. `obj` содержит в себе классы, расширяющие объектную модель `pm4py`;
5. `order_settings` содержит определение интерфейса настроек порядка и его реализаций;
6. `unfolding_algorithms` содержит в себе реализацию 2-х версий алгоритма Макмиллана - стандартный обобщенный (`standard.py`) и обобщенный алгоритм построения развертки сопряженной сети (папка `n_safe`)

В `example.py` содержится пример использования библиотеки
