from pm4py.objects.petri_net.utils import petri_utils

from ..alg import Co, PriorityQueue, update_possible_extensions
from ..decorations import IdleDecorations
from ..obj import Prefix, Event, Condition


def build_prefix(net, m0, order_settings, cutoff_settings, decorations=None, event_count=None,
                 pe_optimise_local_config=True):
    """
    Строит канонический префикс развертки данной сети (при правильно определенном контексте срезания, за который
    отвечают аргументы order_settings и cutoff_settings)
    :param net: сеть Петри
    :param m0: начальная разметка net
    :param order_settings: настройки порядка
    :param cutoff_settings: настройки срезания
    :param decorations: декорации (опционально)
    :param event_count: максимальное количество событий в префиксе. Если построение префикса не закончится до того,
    :param pe_optimise_local_config: аргумент для инициализации PriorityQueue
    как количество событий в префиксе превысит данное значение, построение префикса прекратится и значение флага
    finished будет False. Если не передать event_count, ограничения на количество событий не будет
    :return: префикс развертки
    """
    if event_count is not None and event_count <= 0:
        raise ValueError("event count must be positive")
    if decorations is None:
        decorations = IdleDecorations()

    res = Prefix(net.name)  # В res будет находиться итоговый префикс

    e = Event(None)  # "Изначальное" событие \bot. Его post_set-ом будут условия, соответствующе начальной разметке
    bot = e
    res.add_event(e)

    co = Co()
    pe = PriorityQueue(order_settings, optimise_local_config=pe_optimise_local_config)

    for p in m0.elements():  # Добавление условий, соответствующих начальной разметке
        c = Condition(p)
        res.add_condition(c)
        petri_utils.add_arc_from_to(e, c, res)
        decorations.add_condition(c)
        decorations.add_starting_condition(c)

    # Обновление отношения co, очереди pe и настроек срезания
    co.update(e, res.places)
    cutoff_settings.update(e, order_settings, mark=m0)
    update_possible_extensions(pe, e, res.places, co)

    count = 0
    finished = True
    while pe:  # Пока к префиксу можно добавить новые события
        e, pre = pe.pop()  # Извлекаем минимальное событие

        # Добавляем к префиксу выбранное событие и дуги к нему от условий в его preset-е
        res.add_event(e)
        for c in pre:
            petri_utils.add_arc_from_to(c, e, res)

        # Создаём условия, соответствующие позициям из post_set-а перехода, представленного выбранным событием
        for a in e.transition.out_arcs:
            for _ in range(a.weight):
                c = Condition(a.target)
                res.add_condition(c)
                petri_utils.add_arc_from_to(e, c, res)
                decorations.add_condition(c)

        # Проверяем, является ли событие отсечкой
        is_cutoff, hint = cutoff_settings.check_cutoff(e, order_settings)
        decorations.add_event(e)
        if not is_cutoff:
            # Если нет, обновляем co и pe
            concurrent_with = co.update(e, res.places)
            cutoff_settings.update(e, order_settings, **hint)
            update_possible_extensions(pe, e, concurrent_with, co)
            count += 1
            if event_count is not None and pe and count >= event_count:  # Проверяем, что не превышен предел
                # количества событий
                finished = False
                break
        else:
            # Иначе добавляем в cutoff_events
            res.add_cutoff(e)
            decorations.add_cutoff_event(e)

    # После процедуры удаляем событие bot из префикса
    for a in bot.out_arcs:
        a.target.in_arcs.remove(a)
        res.arcs.remove(a)

    res.transitions.remove(bot)

    res.finished = finished

    return res
