from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to, add_place, add_transition


def generate_milners_cyclic_scheduler(n, round_cap=None):
    """
    Генерирует сеть Петри модели циклического планировщика Мильнера
    :param n: количество рабочих
    :param round_cap: если передано, в сеть добавляется позиция, ограничивающая количество раундов
    :return: сеть Петри, начальная разметка
    """
    net = PetriNet(f"Milner's scheduler {n}")

    def place(x):
        return add_place(net, x)

    def trans(x):
        return add_transition(net, x, x)

    def arc(f, t):
        return add_arc_from_to(f, t, net)

    marking = Marking()

    ready_st = [place(f"ready st{x}") for x in range(1, n + 1)]
    ready_nr = [place(f"ready nr{x}") for x in range(1, n + 1)]

    ready_new = place("ready_new")
    marking[ready_new] += 1

    new_round = trans("new round")
    arc(ready_new, new_round)
    arc(new_round, ready_st[0])
    arc(new_round, ready_nr[0])

    if round_cap is not None:
        rounds = place("rounds")
        marking[rounds] = round_cap
        arc(rounds, new_round)

    for i in range(1, n + 1):
        my_ready_st = ready_st[i - 1]
        my_ready_nr = ready_nr[i - 1]

        next_ready_st = None if i == n else ready_st[i]
        next_ready_nr = ready_new if i == n else ready_nr[i]

        ready = place(f"ready{i}")
        working = place(f"working{i}")
        finished = place(f"finished{i}")

        marking[ready] += 1

        work = trans(f"work{i}")
        finish = trans(f"finish{i}")
        next_round = trans(f"next{i}")

        arc(my_ready_st, work)
        arc(ready, work)
        arc(work, working)
        if next_ready_st is not None:
            arc(work, next_ready_st)

        arc(working, finish)
        arc(finish, finished)

        arc(finished, next_round)
        arc(my_ready_nr, next_round)
        arc(next_round, ready)
        arc(next_round, next_ready_nr)

    return net, marking
