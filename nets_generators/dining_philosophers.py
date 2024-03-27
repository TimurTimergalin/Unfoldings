from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to, add_place, add_transition


def generate_dining_philosophers(n, add_host=False):
    """
    Генерирует сеть Петри, моделирующую задачу об обедающих философах
    :param n: количество философов
    :param add_host: если True, генерируется версия с хостом
    :return: сеть Петри и её начальную разметку
    """
    net = PetriNet(f"Dining philosophers {n}")

    def place(x):
        return add_place(net, x)

    def trans(x, label):
        return add_transition(net, x, label)

    def arc(f, t):
        return add_arc_from_to(f, t, net)

    marking = Marking()

    chopsticks = [place(f"chopstick{x}") for x in range(1, n + 1)]
    marking.update(chopsticks)

    if add_host:
        host = place("host")
        marking[host] = n - 1

    for i in range(1, n + 1):
        chopstick1 = chopsticks[i - 1]
        chopstick2 = chopsticks[i % n]

        thinking = place(f"thinking{i}")
        prepare_left = place(f"prep l{i}")
        prepare_right = place(f"prep r{i}")
        ready_left = place(f"ready l{i}")
        ready_right = place(f"ready r{i}")
        dining = place(f"dining{i}")

        marking[thinking] += 1

        prepare = trans(name := f"prep{i}", label=name)
        take_left = trans(name := f"take l{i}", label=name)
        take_right = trans(name := f"take r{i}", label=name)
        eat = trans(name := f"eat{i}", label=name)
        think = trans(name := f"think{i}", label=name)

        arc(thinking, prepare)
        if add_host:
            arc(host, prepare)

        arc(prepare, prepare_left)
        arc(prepare, prepare_right)

        arc(prepare_left, take_left)
        arc(chopstick1, take_left)
        arc(take_left, ready_left)

        arc(prepare_right, take_right)
        arc(chopstick2, take_right)
        arc(take_right, ready_right)

        arc(ready_left, eat)
        arc(ready_right, eat)
        arc(eat, dining)

        arc(dining, think)
        arc(think, chopstick1)
        arc(think, chopstick2)
        arc(think, thinking)

        if add_host:
            arc(think, host)

    return net, marking
